
"""
python script for continuously fetching data from Elia
"""

import pandas as pd
import requests
import datetime

from src.data_download.data_download import quarter_hour_down_rounder

current_time = datetime.datetime.now()
current_time_UTC = current_time - datetime.timedelta(hours=1) # TODO: somehow account for annual summer time changes
current_time_UTC_dalayed = current_time_UTC - datetime.timedelta(minutes=15) # time delay is cca 30 minutes
current_time_UTC_dalayed_rounded = quarter_hour_down_rounder(current_time_UTC_dalayed)

selected_timeslot = current_time_UTC_dalayed_rounded.strftime("%Y-%m-%dT%H:%M:%S")


# URL for the Elia Wind Power Data:
API_URL = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods086/records?limit=20"

# SQL query
params = {
    "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
    "where" : {f"offshoreonshore = 'Offshore' and datetime = date'{selected_timeslot}'"}
}

url = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods086/records?limit=20"

response = requests.get(API_URL,params=params)
#response = requests.get(API_URL)

data = response.json()
#aa = data['results'][0]

# creating a pandas df for the results
fetched_entry = pd.DataFrame(data = data['results'][0], index=[0])
col_names = ["datetime","offshoreonshore","realtime","monitoredcapacity"]#print(f"response status code: {response.status_code}")
fetched_entry = fetched_entry.reindex(columns=col_names)

#print(data)
print(f"current UTC time: {current_time_UTC}")
print(fetched_entry)


#print("hello there my beautiful")

# params = {
#     "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
#     "where" : {"offshoreonshore = 'Offshore' and datetime = date'2025-03-28T12:30:00+00:00'"}
# }

# params = {
#     "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
#     "where" : {"offshoreonshore = 'Offshore' and datetime = date'2025-03-28T12:30:00'"}
# }