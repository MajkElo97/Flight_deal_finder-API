from twilio.rest import Client
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()
SENDER = "YOUR EMAIL HERE"


# This class is responsible for sending notifications with the deal flight details.
class NotificationManager:

    def __init__(self):
        self.message = None
        self.client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))

    def send_sms(self, city):
        self.message = f"Low price alert! Only {city['price']}GBP " \
                       f"to fly from {city['city_from']}-{city['airport_from']}" \
                       f" to {city['city_to']}-{city['airport_to']} from {city['date_from'].split('T')[0]} " \
                       f"to {city['date_to'].split('T')[0]} via {city['via_city']}"
        print(self.message)
        message = self.client.messages.create(body=self.message, from_='+18158531321', to='+48516154328')
        print(message.status)

    def send_email(self, emails, city):
        # receiver = "m.ociepka@wolftech.pl"
        self.message = f"Low price alert! Only {city['price']}GBP to fly from {city['city_from']}" \
                       f"-{city['airport_from']} to {city['city_to']}-{city['airport_to']} from " \
                       f"{city['date_from'].split('T')[0]} to {city['date_to'].split('T')[0]} via {city['via_city']}"
        try:
            with smtplib.SMTP("YOUR EMAIL DOMAIN HERE", 587) as connection:
                connection.starttls()
                connection.login(user=SENDER, password=os.environ.get("EMAIL_PASSWORD"))
                for email in emails:
                    connection.sendmail(SENDER, email,
                                        msg=f"Subject:New Low Price Flight!\n\n{self.message}".encode('utf-8'))
                    print("Successfully sent email")
        except smtplib.SMTPException:
            print("Error: unable to send email")
