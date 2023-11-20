from datetime import datetime, timedelta
from ..models import UserTrials
from ..serializers import UserTrialSerializer

def schedule_reminder(company, time, userid):
    current_date = datetime.now()

    # Check if time is a relative time
    if "+" in time or "-" in time:
        try:
            # Convert relative time to actual date
            delta_days = int(time)
            reminder_date = current_date + timedelta(days=delta_days)
        except ValueError as e:
            return f"Error processing the request: {e}"
    else:
        # Parse explicit dates like "11/11"
        day, month = map(int, time.split('/'))
        try:
            # Extract day and month, combine with current year
            reminder_date = datetime(current_date.year, month, day)
            
            # If parsed date is in the past for the current year, notify the user
            if reminder_date < current_date:
                return "The provided date has already passed. Please specify a future date."
        except ValueError as e:
            return f"Error processing the request: {e}"
        except IndexError:
            return "Invalid date format. Please provide a valid date."

    formatted_date = reminder_date.strftime('%d/%m/%Y')
    return f"Reminder set for {formatted_date}"


def query_all_subscriptions(userid):
    #retrieves all user subscription using the userId
    list= UserTrials.objects.filter( postedBy = userid)
    serializer= UserTrialSerializer(list,many=True)
    return serializer.data

def get_subscription_details(company,userid):
    #filters userTrial object taking two conditions service name & userId
    subscription= UserTrials.objects.filter( postedBy = userid, name=company.capitalize())
    serializer= UserTrialSerializer(subscription,many=True)
    #TODO: function currently returns Json, what happens if a user asks the question 
    # when is my netflix subscription ending
    # answer should be : your Netflix will be ending on 15 days from now 15th of September
    return serializer.data