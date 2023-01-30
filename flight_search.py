import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

ORIGIN_CITY = "KTW"
MINIMUM_NIGHTS = 7
MAXIMUM_NIGHTS = 28
DAYS_FROM_NOW = 2

load_dotenv()
# TEQUILA_API_HEADER = {"apikey": os.environ.get("TEQUILA_API_TOKEN"), }
TEQUILA_API_HEADER = {"apikey": "YOUR API KEY"}


# This class is responsible for talking to the Flight Search API.
class FlightSearch:

    def __init__(self):
        self.response_flight_tequila = None
        self.tequila_flight_api_parameters = None
        self.iata_code = None
        self.response_iata_tequila = None
        self.tequila_iata_api_parameters = None
        self.all_flights_data = None

    def get_iata(self, city):
        self.tequila_iata_api_parameters = {
            "term": city,
        }
        self.response_iata_tequila = requests.get(url=f"{os.environ.get('TEQUILA_API_ENDPOINT')}/locations/query",
                                                  params=self.tequila_iata_api_parameters, headers=TEQUILA_API_HEADER)
        self.response_iata_tequila.raise_for_status()
        self.response_iata_tequila = self.response_iata_tequila.json()
        self.iata_code = self.response_iata_tequila["locations"][0]["code"]

    def get_data(self, sheety_data):
        self.all_flights_data = []
        today = datetime.now()
        date = today.strftime("%d/%m/%Y")
        future_date = today + timedelta(days=DAYS_FROM_NOW)
        future_date = future_date.strftime("%d/%m/%Y")
        for city in sheety_data:
            print(city)
            self.tequila_flight_api_parameters = {
                "fly_from": ORIGIN_CITY,
                "fly_to": city["iataCode"],
                "date_from": date,
                "date_to": future_date,
                "nights_in_dst_from": MINIMUM_NIGHTS,
                "nights_in_dst_to": MAXIMUM_NIGHTS,
                "flight_type": "round",
                "max_stopovers": 2,
                "curr": "GBP"
            }
            self.response_flight_tequila = requests.get(url=f"{os.environ.get('TEQUILA_API_ENDPOINT')}/v2/search",
                                                        params=self.tequila_flight_api_parameters,
                                                        headers=TEQUILA_API_HEADER)
            try:
                if len(self.response_flight_tequila.json()["data"][0]) != 0:
                    try:
                        self.all_flights_data.append(self.response_flight_tequila.json()["data"])
                    except requests.exceptions.JSONDecodeError:
                        self.tequila_flight_api_parameters["max_stopovers"] = 3
                        self.response_flight_tequila = requests.get(
                            url=f"{os.environ.get('TEQUILA_API_ENDPOINT')}/v2/search",
                            params=self.tequila_flight_api_parameters,
                            headers=TEQUILA_API_HEADER)
                        self.all_flights_data.append(self.response_flight_tequila.json()["data"])

            except IndexError:
                pass
