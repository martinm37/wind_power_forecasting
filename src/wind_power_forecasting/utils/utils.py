

"""
miscellaneous util functions and classes
"""

import datetime

from src.data_download.data_download import quarter_hour_down_rounder


class StatisticalModelSolution:

    def __init__(self,beta_vector, Y_mat, Y_mat_fitted, errors_vector):
        self.beta_vector = beta_vector
        self.Y_mat = Y_mat
        self.Y_mat_fitted = Y_mat_fitted
        self.errors_vector = errors_vector


def adjusted_current_time():

    """
    returns the current time minus 15 minutes to take into account the delay
    in data publishing
    is in UTC timezone, but without the append
    """

    current_time = datetime.datetime.now()

    # winter time
    # current_time_UTC = current_time - datetime.timedelta(hours=1)

    # summer time
    current_time_UTC = current_time - datetime.timedelta(hours=2)

    current_time_UTC_dalayed = current_time_UTC - datetime.timedelta(minutes=15)  # time delay is cca 15 minutes
    current_time_UTC_dalayed_rounded = quarter_hour_down_rounder(current_time_UTC_dalayed)

    selected_timeslot_str = current_time_UTC_dalayed_rounded.strftime("%Y-%m-%dT%H:%M:%S")
    selected_timeslot_datetime = current_time_UTC_dalayed_rounded.replace(microsecond=0)

    return selected_timeslot_str,selected_timeslot_datetime


class UpToDateDataTester:

    def __init__(self,sql_functions_wrapper):
        self.sql_functions_wrapper = sql_functions_wrapper

    def test_for_already_present_monitored_capacity(self,selected_timeslot_datetime):

        """
        I could do INSERT IGNORE INTO query instead, But I do want to know if there was an attempt for
        a connection to DB or not, so I will rather do it like this
        """

        # data already present test

        select_query = ("""
                        SELECT *
                        FROM wind_power_transformed_tbl
                        ORDER BY datetime DESC
                        LIMIT 1
                        """)

        query_data = tuple() # an empty tuple of length 0, for compatibility

        cnx_object, cursor_object = self.sql_functions_wrapper.select_query_wrapper(query_text=select_query,
                                                                                    query_data=query_data)

        latest_record = cursor_object.fetchall()
        #latest_record = select_query_for_latest_full_record()

        latest_record_datetime = latest_record[0][0]
        latest_record_power = latest_record[0][1]
        latest_record_monitored_capacity = latest_record[0][2]
        latest_record_rescaled_power = latest_record[0][3]

        if ((selected_timeslot_datetime == latest_record_datetime)
                and (latest_record_monitored_capacity is not None)):
            return True

        else:
            return False


    def test_for_already_present_full_record(self,selected_timeslot_datetime):

        """
        Because of INSERT IGNORE INTO query I only insert the monitored_capacity once.
        But for the rest of the data I use the UPDATE query. Therefore, I use this test
        to see if 1) there is already a record with the current time and 2) all of the data
        are not NULL. If these two conditions are true, we do not update
        """

        # data already present test
        select_query = ("""
                        SELECT *
                        FROM wind_power_transformed_tbl
                        ORDER BY datetime DESC
                        LIMIT 1
                        """)

        query_data = tuple() # an empty tuple of length 0, for compatibility

        cnx_object, cursor_object = self.sql_functions_wrapper.select_query_wrapper(query_text=select_query,
                                                                                    query_data=query_data)

        latest_record = cursor_object.fetchall()

        #latest_record = select_query_for_latest_full_record()


        latest_record_datetime = latest_record[0][0]
        latest_record_power = latest_record[0][1]
        latest_record_monitored_capacity = latest_record[0][2]
        latest_record_rescaled_power = latest_record[0][3]

        if ((selected_timeslot_datetime == latest_record_datetime)
                and (latest_record_power is not None)
                and (latest_record_monitored_capacity is not None)
                and (latest_record_rescaled_power is not None)):
            return True
        else:
            return False





