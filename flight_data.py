from datetime import datetime, timedelta
from pprint import pprint


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.cheapest_flights = None
        self.flight = None
        self.city_flights_list = []
        self.all_city_flights_list = []

    def convert_data(self, data):
        for city in data:
            self.city_flights_list = []
            for flight in city:
                city_from = flight["cityFrom"]
                city_from_code = flight["cityCodeFrom"]
                city_to = flight["cityTo"]
                city_to_code = flight["cityCodeTo"]
                airport_from = flight["flyFrom"]
                airport_to = flight["flyTo"]
                price = flight["price"]
                link = flight["deep_link"]
                date_split = flight["local_arrival"].split('T')[0].split("-")
                date_from = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
                date_to = date_from + timedelta(days=flight["nightsInDest"])
                if len(flight["route"]) > 2:
                    via_city = flight["route"][0]["cityTo"]
                else:
                    via_city = "No transit city"
                date_from = date_from.strftime("%d/%m/%Y")
                date_to = date_to.strftime("%d/%m/%Y")
                self.flight = {"city_from": city_from,
                               "city_from_code": city_from_code,
                               "city_to": city_to,
                               "city_to_code": city_to_code,
                               "airport_from": airport_from,
                               "airport_to": airport_to,
                               "price": price,
                               "link": link,
                               "date_from": date_from,
                               "date_to": date_to,
                               "via_city": via_city,
                               }
                self.city_flights_list.append(self.flight)
            self.all_city_flights_list.append(self.city_flights_list)
        pprint(self.all_city_flights_list)

    def find_cheapest(self):
        self.cheapest_flights = [city[0] for city in self.all_city_flights_list]
