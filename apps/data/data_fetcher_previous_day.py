
"""
python script for fetching up last 100 available data points from Elia -> cca. the current day (96 quarters)
-> but it seems that data in this dataset is always available only from 22.00 of the previous day, not earlier
"""

import requests
import datetime
import pandas as pd
import numpy as np


from src.data_download.data_download import quarter_hour_down_rounder
from src.mysql_query_functions.mysql_query_functions import delete_query,pandas_df_insert_query


def data_fetch_previous_day_function():

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

    # setting this to the 22.00 of the previous day
    current_day = current_time_UTC_dalayed_rounded.day
    current_time_UTC_shifted = \
        current_time_UTC_dalayed_rounded.replace(day=current_day-1,hour=22,minute=0,second=0,microsecond=0)
    """
    dataset is until 22.00 of the previous day
    """

    selected_timeslot = current_time_UTC_shifted.strftime("%Y-%m-%dT%H:%M:%S")

    # URL for the Elia Wind Power Data:
    API_URL = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods031/records?limit=100"

    # SQL query
    params = {
        "select" : {"datetime","offshoreonshore","measured","monitoredcapacity"},
        "where" : {f"offshoreonshore = 'Offshore' and datetime < date'{selected_timeslot}'"}
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

        data_df = data_df.rename(columns={"measured": "realtime"})

        # changing the order of columns
        col_names = ["datetime","offshoreonshore","realtime","monitoredcapacity"]
        data_df = data_df.reindex(columns=col_names)

        # work on the time column, ordering by datetime in desc order
        data_df["datetime"] = pd.to_datetime(data_df["datetime"], utc=True)  # converting to time
        data_df['datetime'] = data_df['datetime'].dt.tz_convert(None)
        data_df = data_df.sort_values(by="datetime", ascending=False)

        """
        After sorting I have to reset the index!!!!!!, Otherwise then can be problems down the line!!
        """
        data_df = data_df.reset_index(drop=True)

        # dropping the unnecessary column
        data_df = data_df.drop(columns="offshoreonshore")

        data_df = data_df.rename(
            columns={"datetime": "datetime",
                     "realtime": "measured_and_upscaled",
                     "monitoredcapacity": "monitored_capacity"})

        """
        in this data set the monitored capacity _is_ always present
        """

        # numpy operations
        monitored_capacity = data_df["monitored_capacity"].iloc[0]
        measured_and_upscaled_vec = data_df["measured_and_upscaled"].to_numpy()
        measured_and_upscaled_vec = np.minimum(np.maximum(measured_and_upscaled_vec,0),monitored_capacity) # bounding the power vector
        monitored_capacity_vec = data_df["monitored_capacity"].to_numpy()
        rescaled_power_vec = measured_and_upscaled_vec / monitored_capacity_vec * 100

        data_df["measured_and_upscaled"] = pd.Series(measured_and_upscaled_vec)
        data_df["monitored_capacity"] = pd.Series(monitored_capacity_vec)
        data_df["rescaled_power"] = pd.Series(rescaled_power_vec)

        """
        As there is no UPDATE option for pandas .to_sql() method, I will do the updating by
        first deleting all of the observations within the given time frame of the new data, and
        then inserting the new data
        """

        # I had to do this convoluted mess for a single datetime value, to remove the timezone and convert it to datetime
        datetime_end = pd.to_datetime(data_df["datetime"].iloc[0], utc=True)
        datetime_end = datetime_end.tz_convert(None)
        datetime_end = datetime_end.to_pydatetime()

        datetime_start = pd.to_datetime(data_df["datetime"].iloc[-1], utc=True)
        datetime_start = datetime_start.tz_convert(None)
        datetime_start = datetime_start.to_pydatetime()

        # UPDATING DATA
        # --------------------------------------------

        # deleting original
        delete_query(datetime_start, datetime_end)

        # inserting new
        pandas_df_insert_query(data_df)



if __name__ == "__main__":
    data_fetch_previous_day_function()



