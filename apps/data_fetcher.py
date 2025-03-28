
"""
python script for continuously fetching data from Elia
"""

import requests
import datetime

from src.data_download.data_download import quarter_hour_down_rounder

current_time = datetime.datetime.now()
current_time_UTC = current_time - datetime.timedelta(hours=1) # TODO: somehow account for annual summer time changes
current_time_UTC_dalayed = current_time_UTC - datetime.timedelta(minutes=30) # time delay is cca 30 minutes
current_time_UTC_dalayed_rounded = quarter_hour_down_rounder(current_time_UTC_dalayed)

selected_timeslot = current_time_UTC_dalayed_rounded.strftime("%Y-%m-%dT%H:%M:%S")


# URL for the Elia Wind Power Data:
API_URL = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods086/records?limit=10"

# SQL query
params = {
    "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
    "where" : {f"offshoreonshore = 'Offshore' and datetime = date'{selected_timeslot}'"},
    "order by": {"realtime DESC"}
}

url = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods086/records?limit=20"

response = requests.get(API_URL,params=params)
#response = requests.get(API_URL)

data = response.json()

print(f"response status code: {response.status_code}")
print(data)


#print("hello there my beautiful")

# params = {
#     "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
#     "where" : {"offshoreonshore = 'Offshore' and datetime = date'2025-03-28T12:30:00+00:00'"}
# }

# params = {
#     "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
#     "where" : {"offshoreonshore = 'Offshore' and datetime = date'2025-03-28T12:30:00'"}
# }