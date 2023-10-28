import openai
import os
from functions import schedule_reminder, query_all_subscriptions, get_subscription_details
from prompts import INIT_PROMPT
from datetime import datetime, timedelta

class Chatbot:
    # Shared configuration (constant for all instances)
    API_KEY = os.getenv("OPENAI_API_KEY")
    FUNCTIONS = ["schedule_reminder:company:datetime", "query_all_subscriptions", "get_subscription_details:company", "unrecognised"]
    FUNCTION_MAP = {
        "schedule_reminder": schedule_reminder,
        "query_all_subscriptions": query_all_subscriptions,
        "get_subscription_details": get_subscription_details
    }
    
    def __init__(self):
        
        openai.api_key = self.API_KEY
        self.messages = [{"role": "system", "content": INIT_PROMPT.format(Chatbot.FUNCTIONS)}]
        self.back_and_forth = 0
    
    def get_response(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        self.back_and_forth += 1

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        response = completion.choices[0].message['content']
        self.back_and_forth += 1

        function_name = response.split(":")[0]
        
        if function_name in self.FUNCTION_MAP:
            try:
                # Use get_function_response to get the response and validate parameters
                actual_response = self._get_function_response(function_name, response)
                self._reset_chat()
                return actual_response
            except ValueError as e:
                return f"Error processing the request: {e}. Please provide more information."

        elif self.back_and_forth >= 7 or function_name in ["unrecognised", "irrelevant"]:
            self._reset_chat()
            return "Let's start over. Please state your request again."

        return response
    
    def _get_function_response(self, function_name, response):
        if function_name == "schedule_reminder":
            _, company, time = response.split(":", 2)
            if not company or not time:
                raise ValueError("Incomplete information. Please specify both the company and time.")
            return schedule_reminder(company, time)

        elif function_name == "get_subscription_details":
            _, company = response.split(":", 1)
            if not company:
                raise ValueError("Incomplete information. Please specify the company.")
            return get_subscription_details(company)

        else:
            return self.FUNCTION_MAP[function_name]()
    
    def _reset_chat(self):
        self.messages.clear()
        self.messages.append({"role": "system", "content": INIT_PROMPT.format(Chatbot.FUNCTIONS)})
        self.back_and_forth = 0


# For testing
if __name__ == "__main__":
    chatbot = Chatbot()
    
    # First interaction
    query1 = "Can you schedule a reminder for a week from now"
    print(f"User:", query1)
    print(f"Chatbot:", chatbot.get_response(query1))

    # # Second interaction
    query2 = "amazon"
    print(f"User:", query2)
    print(f"Chatbot:", chatbot.get_response(query2)) 

    # # # Third interaction
    # query3 = "yes"
    # print(f"User:", query3)
    # print(f"Chatbot:", chatbot.get_response(query3))
