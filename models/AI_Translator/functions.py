from datetime import datetime, timedelta
import re

def schedule_reminder(company, time):
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


def query_all_subscriptions():
	print("hello all")
	return "you pay $4000 a month"

def get_subscription_details(company):
	print(company)
	return "you pay $300 a month for Amazon Prime"