from datetime import datetime, timedelta

#functions go here

def schedule_reminder(company, time):
    # Check if time is a relative time
    if "+" in time or "-" in time:
        try:
            # Convert relative time to actual date
            delta_days = int(time)
            reminder_date = datetime.now() + timedelta(days=delta_days)
            formatted_date = reminder_date.strftime('%d/%m/%Y')
        except ValueError as e:
            return f"Error processing the request: {e}"
    else:
        formatted_date = time 

    print(f"Reminder scheduled for {company} on {formatted_date}")
    return f"Reminder scheduled for {company} on {formatted_date}"


def query_all_subscriptions():
	print("hello all")
	return "you pay $4000 a month"

def get_subscription_details(company):
	print(company)
	return "you pay $300 a month for Amazon Prime"