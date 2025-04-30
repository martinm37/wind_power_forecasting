
"""
python script for fetching up last 100 available data points from Elia -> cca. the current day (96 quarters)
"""

import requests
import datetime
import pandas as pd


from src.data_download.data_download import quarter_hour_down_rounder


def data_fetch_current_day_function():

    exit_status = "" #will contain which branch got executed


    current_time = datetime.datetime.now()

    # winter time
    #current_time_UTC = current_time - datetime.timedelta(hours=1)

    # summer time
    current_time_UTC = current_time - datetime.timedelta(hours=2)

    """
    here I delay by 30 minutes, 15 mins extra when compared to data_fetcher.py
    """

    current_time_UTC_dalayed = current_time_UTC - datetime.timedelta(minutes=30)
    current_time_UTC_dalayed_rounded = quarter_hour_down_rounder(current_time_UTC_dalayed)

    selected_timeslot = current_time_UTC_dalayed_rounded.strftime("%Y-%m-%dT%H:%M:%S")

    selected_timeslot_datetime = pd.to_datetime(selected_timeslot ,utc=True)
    selected_timeslot_datetime = selected_timeslot_datetime.tz_convert(None)
    selected_timeslot_datetime = selected_timeslot_datetime.to_pydatetime()

    # URL for the Elia Wind Power Data:
    API_URL = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods086/records?limit=100"

    # SQL query
    params = {
        "select" : {"datetime","offshoreonshore","realtime","monitoredcapacity"},
        "where" : {f"offshoreonshore = 'Offshore' and datetime <= date'{selected_timeslot}'"}
    }

    try:
        response = requests.get(API_URL,params=params)

    except requests.exceptions.RequestException as api_conn_err:

        print(api_conn_err)
        exit_status = "api_connection_error"
        return exit_status
        # raise SystemExit(api_conn_err)

    else:

        data = response.json()
        data_df = pd.DataFrame(data=data['results'])

        # changing the order of columns
        col_names = ["datetime","offshoreonshore","realtime","monitoredcapacity"]
        data_df = data_df.reindex(columns=col_names)

        # work on the time column, ordering by datetime in desc order
        data_df["datetime"] = pd.to_datetime(data_df["datetime"], utc=True)  # converting to time
        data_df['datetime'] = data_df['datetime'].dt.tz_convert(None)
        data_df = data_df.sort_values(by="datetime", ascending=False)

        # dropping the unnecessary column
        data_df = data_df.drop(columns="offshoreonshore")

        """
        next steps: obtain the monitored capacity
        overwrite the column with it
        create the rescaled power column
        update the rows in DB: first delete them, then insert the new ones
        """





if __name__ == "__main__":
    exit_state = data_fetch_current_day_function()
    print(datetime.datetime.now(),exit_state)


