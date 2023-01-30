import requests
import os
from dotenv import load_dotenv

load_dotenv()
SHEETY_API_HEADER = {"Authorization": os.environ.get("SHEETY_API_TOKEN"), }


# This class is responsible for talking to the Google Sheet and adding users.
class Users:
    def __init__(self):
        self.sheety_api_parameters = None
        self.emails = None
        self.response_send_sheety = None

    def add_user(self):
        print("Welcome to Michael flight's club\nWe find the best deals for you!")
        name = input("What is your first name: ")
        last_name = input("What is your last name: ")
        email = input("What is your email: ")
        email2 = input("Type your email again: ")
        while email != email2:
            print("Email's do not match")
            email = input("What is your email? ")
            email2 = input("Can you repeat the email? ")

        self.sheety_api_parameters = {
            "user": {
                "firstName": name,
                "lastName": last_name,
                "email": email,
            }
        }
        self.response_send_sheety = requests.post(url=os.environ.get("SHEETY_API_ENDPOINT_USERS"),
                                                  json=self.sheety_api_parameters,
                                                  headers=SHEETY_API_HEADER)
        self.response_send_sheety.raise_for_status()
        self.response_send_sheety.text
        print("You are in the club!")

    def get_emails(self):
        response_receive_sheety = requests.get(url=os.environ.get("SHEETY_API_ENDPOINT_USERS"),
                                               headers=SHEETY_API_HEADER)
        response_receive_sheety.raise_for_status()
        response_receive_sheety = response_receive_sheety.json()["users"]
        self.emails = [user["email"] for user in response_receive_sheety]
        return self.emails
