import logging
import os
import pytz
import schedule
import time

from datetime import datetime, timezone
from gmail import Gmail


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())


def send_email() -> None:
    """Send an email with the specified subject and body content.
    
    Returns:
        None
    """
    # Email configuration
    gmail = Gmail(
        gmail_username=os.environ.get('GMAIL_USERNAME'),
        gmail_password=os.environ.get('GMAIL_PASSWORD')
    )

    # Email content
    recipients = os.getenv("RECIPIENTS", "").replace(" ", "").split(",")
    subject = 'ACTIVATE WORKOUT MODE: LEGENDARY'
    with open('email_body.html', 'r') as file:
        body = file.read()

    # Send the email
    gmail.set_recipients(recipients)
    gmail.set_subject(subject)
    gmail.add_html(body)
    gmail.send_email()
    
    # Get the current time in UTC
    now_utc = datetime.now(timezone.utc)
    formatted_utc_time = now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')
    logger.info(f"Email sent to {recipients} at {formatted_utc_time}.")


def run() -> None:       
    """Entrypoint for the script.
    
    Returns:
        None
    """
    # Schedule the email to be sent daily at whatever time the user specifies
    # I want an exception to be raised if the user doesn't provide this.s
    time_in_utc = os.environ["TIME_IN_UTC"]
    schedule.every().day.at(time_in_utc, tz=pytz.utc).do(send_email)

    # Run the scheduler on an infinite loop, or until the user interrupts the 
    # script (Ctrl+C)
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("Goodbye!")


def help():
    print("This script is a simple email service that sends an email with a specified subject and body content.")
    print("To use this script, you need to set the following environment variables:")
    print("- GMAIL_USERNAME: Your Gmail username")
    print("- GMAIL_PASSWORD: Your Gmail password")
    print("- RECIPIENTS: Comma-separated list of email recipients (e.g., RECIPIENTS=\"scott@me.com, john@me.com\")")
    print("- TIME_IN_UTC: The time in UTC (HH:MM) at which the email should be sent daily (e.g., TIME_IN_UTC=\"12:05\" for 12:05 UTC)")
    print("\nExample Usage (CLI):")
    print("$ GMAIL_USERNAME=sender_email@me.com GMAIL_PASSWORD=\"senderemailpassword\" RECIPIENTS=\"scott@me.com, john@me.com\" TIME_IN_UTC=\"03:15\" python main.py")
    print("\nExample Usage (Docker container):")
    print("$ docker build -t email-service-image .")
    print("$ docker run -d --name email-service -e GMAIL_USERNAME=sender_email@me.com -e GMAIL_PASSWORD=\"senderemailpassword\" -e RECIPIENTS=\"scott@me.com, john@me.com\" -e TIME_IN_UTC=\"03:15\" email-service-image")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"An error occurred: {e}\n")
        help()
