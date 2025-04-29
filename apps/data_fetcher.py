
"""
python script for continuously fetching data from Elia
"""

import requests
import datetime
import pandas as pd


from src.data_download.data_download import quarter_hour_down_rounder
from src.mysql_query_functions.mysql_query_functions import insert_query_partial, select_query_for_latest_monitored_capacity, \
    insert_query_full, update_query

current_time = datetime.datetime.now()

# winter time
#current_time_UTC = current_time - datetime.timedelta(hours=1) # TODO: somehow account for annual summer time changes automatically

# summer time
current_time_UTC = current_time - datetime.timedelta(hours=2)

current_time_UTC_dalayed = current_time_UTC - datetime.timedelta(minutes=15) # time delay is cca 15 minutes
current_time_UTC_dalayed_rounded = quarter_hour_down_rounder(current_time_UTC_dalayed)

selected_timeslot = current_time_UTC_dalayed_rounded.strftime("%Y-%m-%dT%H:%M:%S")

selected_timeslot_datetime = pd.to_datetime(selected_timeslot ,utc=True)
selected_timeslot_datetime = selected_timeslot_datetime.tz_convert(None)
selected_timeslot_datetime = selected_timeslot_datetime.to_pydatetime()

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
data_entries = data['results'][0]

# I had to do this convoluted mess for a single datetime value, to remove the timezone and convert it to datetime
data_datetime = pd.to_datetime(data_entries["datetime"] ,utc=True)
data_datetime = data_datetime.tz_convert(None)
data_datetime = data_datetime.to_pydatetime()

data_power = data_entries["realtime"]
data_monitoredcapacity = data_entries["monitoredcapacity"]


"""
There seems to be an issue with real time data: Either "realtime" or "monitoredcapacity" is None, but not both or
neither. 
'Best' solution right now seems to me to store the last "monitoredcapacity" value in the table, and 
retrieve it later
"""

if data_monitoredcapacity is not None:

    """ we insert only this value and the datetime into the db for later use"""

    insert_query_partial(data_datetime, data_monitoredcapacity)


elif (data_power is not None) and (data_monitoredcapacity is None):

    """here we retrieve last known data_monitoredcapacity value and its date and compute and insert the rest"""

    fetched_data = select_query_for_latest_monitored_capacity()


    last_datetime = fetched_data[0][0]
    last_known_monitoredcapacity = fetched_data[0][1]

    # transforming data_realtime
    data_power = min(max(data_power, 0), last_known_monitoredcapacity)
    data_rescaled_power = data_power / last_known_monitoredcapacity * 100

    """if the last_known_monitoredcapacity is from the current quarter, we update records,
     otherwise we insert the whole data, accepting the mismatch"""

    if selected_timeslot_datetime != last_datetime:
        print("There is a datetime mismatch.")
        insert_query_full(data_datetime, data_power, last_known_monitoredcapacity, data_rescaled_power)

    elif selected_timeslot_datetime == last_datetime:
        update_query(data_datetime, data_power, data_rescaled_power)



elif (data_power is not None) and (data_monitoredcapacity is not None):

    """currently (at 2025-04-29) does not happen with real time data"""

    # transforming data_realtime
    data_power = min(max(data_power, 0), data_monitoredcapacity)
    data_rescaled_power = data_power / data_monitoredcapacity * 100

    insert_query_full(data_datetime, data_power, data_monitoredcapacity, data_rescaled_power)













# # creating a pandas df for the results
# fetched_entry = pd.DataFrame(data = data['results'][0], index=[0])
# col_names = ["datetime","offshoreonshore","realtime","monitoredcapacity"]#print(f"response status code: {response.status_code}")
# fetched_entry = fetched_entry.reindex(columns=col_names)
#
# #print(data)
# print(f"current UTC time: {current_time_UTC}")
# print(fetched_entry)


#print("hello there my beautiful")

# params = {
#     "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
#     "where" : {"offshoreonshore = 'Offshore' and datetime = date'2025-03-28T12:30:00+00:00'"}
# }

# params = {
#     "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
#     "where" : {"offshoreonshore = 'Offshore' and datetime = date'2025-03-28T12:30:00'"}
# }