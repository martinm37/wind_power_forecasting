"""
miscellaneous util functions and classes
"""

from datetime import datetime, timedelta, timezone

from src.wind_power_forecasting.data_download.data_download import (
    quarter_hour_down_rounder,
)
from wind_power_forecasting.mysql_query_functions.mysql_query_functions import (
    SQLFunctionsWrapper,
)

UTC_TIMEZONE = timezone(offset=timedelta(hours=0))
CEST_TIMEZONE = timezone(offset=timedelta(hours=2))

class StatisticalModelSolution:
    def __init__(self, beta_vector, Y_mat, Y_mat_fitted, errors_vector):
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

    # TODO: make logic that automatically switches between summer and winter
    current_time = datetime.now(tz=CEST_TIMEZONE)
    current_time_UTC = current_time.astimezone(UTC_TIMEZONE)

    current_time_UTC_dalayed = current_time_UTC - timedelta(
        minutes=15
    )  # time delay is cca 15 minutes
    current_time_UTC_dalayed_rounded = quarter_hour_down_rounder(
        current_time_UTC_dalayed
    )

    selected_timeslot_str = current_time_UTC_dalayed_rounded.strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    selected_timeslot_datetime = current_time_UTC_dalayed_rounded.replace(microsecond=0)

    return selected_timeslot_str, selected_timeslot_datetime


class UpToDateDataTester:
    def __init__(self, sql_functions_wrapper: SQLFunctionsWrapper):
        self.sql_functions_wrapper = sql_functions_wrapper

    def test_for_already_present_monitored_capacity(self, selected_timeslot_datetime):
        """
        I could do INSERT IGNORE INTO query instead, But I do want to know if there was an attempt for
        a connection to DB or not, so I will rather do it like this
        """

        # data already present test

        select_query = """
                        SELECT *
                        FROM wind_power_transformed_tbl
                        ORDER BY datetime DESC
                        LIMIT 1
                        """

        select_query_outputs = self.sql_functions_wrapper.select_query_wrapper(
            query_text=select_query
        )
        cursor_object = select_query_outputs.cursor

        latest_record = cursor_object.fetchall()
        # latest_record = select_query_for_latest_full_record()

        latest_record_datetime = latest_record[0][0]
        latest_record_power = latest_record[0][1]
        latest_record_monitored_capacity = latest_record[0][2]
        latest_record_rescaled_power = latest_record[0][3]

        if (selected_timeslot_datetime == latest_record_datetime) and (
            latest_record_monitored_capacity is not None
        ):
            return True

        else:
            return False

    def test_for_already_present_full_record(self, selected_timeslot_datetime):
        """
        Because of INSERT IGNORE INTO query I only insert the monitored_capacity once.
        But for the rest of the data I use the UPDATE query. Therefore, I use this test
        to see if 1) there is already a record with the current time and 2) all of the data
        are not NULL. If these two conditions are true, we do not update
        """

        # data already present test
        select_query = """
                        SELECT *
                        FROM wind_power_transformed_tbl
                        ORDER BY datetime DESC
                        LIMIT 1
                        """

        select_query_outputs = self.sql_functions_wrapper.select_query_wrapper(
            query_text=select_query,
        )
        cursor_object = select_query_outputs.cursor

        latest_record = cursor_object.fetchall()

        # latest_record = select_query_for_latest_full_record()

        latest_record_datetime = latest_record[0][0]
        latest_record_power = latest_record[0][1]
        latest_record_monitored_capacity = latest_record[0][2]
        latest_record_rescaled_power = latest_record[0][3]

        if (
            (selected_timeslot_datetime == latest_record_datetime)
            and (latest_record_power is not None)
            and (latest_record_monitored_capacity is not None)
            and (latest_record_rescaled_power is not None)
        ):
            return True
        else:
            return False
