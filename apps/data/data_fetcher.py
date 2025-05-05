
"""
python script for fetching data from Elia
- able to be run continuously when run by a cron job through a bash script
"""

import os
import requests
import datetime
import pandas as pd


from src.data_download.data_download import quarter_hour_down_rounder
from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.utils.utils import UpToDateDataTester


# TODO: implement a logger feature
# TODO: somehow account for annual summer time changes automatically


def data_fetch_function(sql_functions_wrapper,up_to_date_data_tester):

    exit_status = "" #will contain which branch got executed


    current_time = datetime.datetime.now()

    # winter time
    #current_time_UTC = current_time - datetime.timedelta(hours=1)

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

    try:
        response = requests.get(API_URL,params=params)

    except requests.exceptions.RequestException as api_conn_err:

        print(api_conn_err)
        exit_status = "api_connection_error"
        return exit_status
        # raise SystemExit(api_conn_err)

    else:

        data = response.json()

        if len(data['results'][0]) == 0:
            # for some reason, this error spontaneously happens and I have no idea why,
            # - it is not caught by RequestException handling
            print("Here is the weird error?")
            print(data)
            print(data['results'])
            exit_status = "zero_length_error"
            return exit_status
        else:
            pass

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

        if (data_power is None) and (data_monitoredcapacity is not None):

            """ we insert only this value and the datetime into the db for later use"""

            test_result = up_to_date_data_tester.test_for_already_present_monitored_capacity(selected_timeslot_datetime)
            #test_result = test_for_already_present_monitored_capacity(selected_timeslot_datetime)

            if test_result:
                #print("monitored capacity data record already present")
                exit_status = "monitored_capacity_already_present"
                return exit_status

            else:

                insert_query = ("""
                                INSERT INTO wind_power_transformed_tbl
                                (datetime, monitored_capacity)
                                VALUES
                                (%s, %s);
                                """)

                query_data = (data_datetime, data_monitoredcapacity)

                sql_functions_wrapper.insert_update_delete_query_wrapper(query_text=insert_query,query_data=query_data)

                #insert_query_partial(data_datetime, data_monitoredcapacity)
                exit_status = "inserted_partial_data"

                return exit_status



        elif (data_power is not None) and (data_monitoredcapacity is None):

            """here we retrieve last known data_monitoredcapacity value and its date and compute and insert the rest"""

            test_result = up_to_date_data_tester.test_for_already_present_full_record(selected_timeslot_datetime)
            #test_result = test_for_already_present_full_record(selected_timeslot_datetime)

            if test_result:
                #print("Full data record already present")
                exit_status = "full_data_already_present"
                return exit_status

            else:

                select_query = ("""
                                SELECT datetime, monitored_capacity
                                FROM wind_power_transformed_tbl
                                ORDER BY datetime DESC
                                LIMIT 1
                                """)

                query_data = tuple()  # an empty tuple of length 0, for compatibility

                cnx_object, cursor_object = sql_functions_wrapper.select_query_wrapper(query_text=select_query,
                                                                                       query_data=query_data)

                fetched_data = cursor_object.fetchall()

                #fetched_data = select_query_for_latest_monitored_capacity()

                last_datetime = fetched_data[0][0]
                last_known_monitoredcapacity = fetched_data[0][1]

                # transforming data_realtime
                data_power = min(max(data_power, 0), last_known_monitoredcapacity)
                data_rescaled_power = data_power / last_known_monitoredcapacity * 100

                """if the last_known_monitoredcapacity is from the current quarter, we update records,
                 otherwise we insert the whole data, accepting the mismatch"""

                if selected_timeslot_datetime != last_datetime:

                    print("There is a datetime mismatch.")

                    insert_query = ("""
                                    INSERT INTO wind_power_transformed_tbl
                                    (datetime, measured_and_upscaled, monitored_capacity, rescaled_power)
                                    VALUES
                                    (%s, %s, %s, %s);
                                    """)

                    query_data = (data_datetime, data_power, data_monitoredcapacity, data_rescaled_power)

                    sql_functions_wrapper.insert_update_delete_query_wrapper(query_text=insert_query,
                                                                             query_data=query_data)

                    #insert_query_full(data_datetime, data_power, last_known_monitoredcapacity, data_rescaled_power)


                    exit_status = "inserted_full_data"
                    return exit_status


                elif selected_timeslot_datetime == last_datetime:

                    update_query = ("""
                                    UPDATE wind_power_transformed_tbl
                                    SET measured_and_upscaled = %s, rescaled_power = %s
                                    WHERE datetime = %s;
                                    """)

                    query_data = (data_power, data_rescaled_power, data_datetime)

                    sql_functions_wrapper.insert_update_delete_query_wrapper(query_text=update_query,
                                                                             query_data=query_data)

                    #update_query(data_datetime, data_power, data_rescaled_power)

                    exit_status = "inserted_full_data"
                    return exit_status




        elif (data_power is not None) and (data_monitoredcapacity is not None):

            """currently (at 2025-04-29) does not happen with real time data"""

            test_result = up_to_date_data_tester.test_for_already_present_full_record(selected_timeslot_datetime)
            #test_result = test_for_already_present_full_record(selected_timeslot_datetime)

            if test_result:
                #print("Full data record already present")
                exit_status = "full_data_already_present"
                return exit_status

            else:

                # transforming data_realtime
                data_power = min(max(data_power, 0), data_monitoredcapacity)
                data_rescaled_power = data_power / data_monitoredcapacity * 100

                insert_query = ("""
                                INSERT INTO wind_power_transformed_tbl
                                (datetime, measured_and_upscaled, monitored_capacity, rescaled_power)
                                VALUES
                                (%s, %s, %s, %s);
                                """)

                query_data = (data_datetime, data_power, data_monitoredcapacity, data_rescaled_power)

                sql_functions_wrapper.insert_update_delete_query_wrapper(query_text=insert_query,
                                                                         query_data=query_data)

                #insert_query_full(data_datetime, data_power, data_monitoredcapacity, data_rescaled_power)

                exit_status = "inserted_full_data"
                return exit_status



if __name__ == "__main__":

    connection_dict = {
        "user": os.environ["STANDARD_USER_1"],
        "password": os.environ["STANDARD_USER_1_PASSWORD"],
        "host": "localhost",
        "port": 3306,
        "database": "wind_power_db",
        "datatable": "wind_power_transformed_tbl"}

    sql_functions_wrapper = SQLFunctionsWrapper(connection_dict = connection_dict)

    up_to_date_data_tester = UpToDateDataTester(sql_functions_wrapper)

    exit_state = data_fetch_function(sql_functions_wrapper,up_to_date_data_tester)
    print(datetime.datetime.now(),exit_state)


