import openai
import os
from functions import schedule_reminder, query_all_subscriptions, get_subscription_details
from prompts import INIT_PROMPT

class Chatbot:
    # Shared configuration (constant for all instances)
    API_KEY = os.getenv("OPENAI_API_KEY")
    FUNCTIONS = ["schedule_reminder:company:datetime", "query_all_subscriptions", "get_subscription_details", "unrecognised"]
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
            if function_name == "schedule_reminder":
                try:
                    _, company, time = response.split(":", 2)
                    actual_response = schedule_reminder(company, time)
                    self._reset_chat()
                    return actual_response
                except ValueError as e:
                    self.messages.append({"role": "assistant", "content": f"Error processing the request: {e}"})
            else:
                actual_response = self.FUNCTION_MAP[function_name]()
                self._reset_chat()
                return actual_response
        elif self.back_and_forth >= 7:
            self._reset_chat()
            return "Let's start over. Please state your request again."
        else:
            self.messages.append({"role": "assistant", "content": response})
        return response
    
    def _reset_chat(self):
        self.messages.clear()
        self.messages.append({"role": "system", "content": INIT_PROMPT.format(Chatbot.FUNCTIONS)})
        self.back_and_forth = 0


# For testing
if __name__ == "__main__":
    chatbot = Chatbot()
    
    # First interaction
    query1 = "can you set a reminder?"
    print(f"User:", query1)
    print(f"Chatbot:", chatbot.get_response(query1))

    # # Second interaction
    query2 = "amazon a week from now"
    print(f"User:", query2)
    print(f"Chatbot:", chatbot.get_response(query2))

    # # # Third interaction
    # query3 = "yes"
    # print(f"User:", query3)
    # print(f"Chatbot:", chatbot.get_response(query3))
