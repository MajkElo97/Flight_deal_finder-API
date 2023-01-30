import requests
import os
from dotenv import load_dotenv

load_dotenv()
SHEETY_API_HEADER = {"Authorization": os.environ.get("SHEETY_API_TOKEN"), }


class DataManager:
    # This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.response_send_sheety = None
        self.response_receive_sheety = None
        self.sheety_api_parameters = None

    def get_data(self):
        self.response_receive_sheety = requests.get(url=os.environ.get("SHEETY_API_ENDPOINT"),
                                                    headers=SHEETY_API_HEADER)
        self.response_receive_sheety.raise_for_status()
        return self.response_receive_sheety.json()["prices"]

    def put_data(self, id_city, iata):
        self.sheety_api_parameters = {
            "price": {
                "iataCode": iata,
            }
        }
        self.response_send_sheety = requests.put(url=f"{os.environ.get('SHEETY_API_ENDPOINT')}/{id_city}",
                                                 json=self.sheety_api_parameters,
                                                 headers=SHEETY_API_HEADER)
        self.response_send_sheety.raise_for_status()
        self.response_send_sheety = self.response_send_sheety.text
