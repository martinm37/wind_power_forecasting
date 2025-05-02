

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





