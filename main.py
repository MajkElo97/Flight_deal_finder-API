# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user_data import Users

users = Users()
data_manager = DataManager()
flight_data = FlightData()
flight_search = FlightSearch()
notification_manager = NotificationManager()

add_user = input("Do You want to add new user?(Type Y/N): ")
if add_user.lower() == "y":
    users.add_user()

sheet_data = data_manager.get_data()

for city in sheet_data:
    if len(city["iataCode"]) == 0:
        flight_search.get_iata(city["city"])
        data_manager.put_data(city["id"], flight_search.iata_code)

flight_search.get_data(sheet_data)
flights_data = flight_search.all_flights_data
flight_data.convert_data(flights_data)
flight_data.find_cheapest()

for city in flight_data.cheapest_flights:
    for target in sheet_data:
        if city["city_to"] == target["city"]:
            if float(city["price"]) <= float(target["lowestPrice"]):
                pass
                notification_manager.send_sms(city)
                notification_manager.send_email(users.get_emails(), city)
