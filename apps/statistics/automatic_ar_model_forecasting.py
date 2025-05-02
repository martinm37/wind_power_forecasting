
"""
this script runs data_fetch_function(), if the exit state of this function states that full data were
inserted for the current time window, it runs the ar_p_model_forecasting() function on this newest data
"""

import datetime

from apps.data.data_fetcher import data_fetch_function
from apps.statistics.ar_model_forecasting import ar_p_model_forecasting

# fetching newest data
# ----------------------
fetching_exit_status = data_fetch_function()
print(datetime.datetime.now(),fetching_exit_status)

# forecasting
# ----------------------
if fetching_exit_status == "inserted_full_data":

    """
    this exit state happens only if full data are inserted for the current time window the first time:
    - it should happen oly once every 15 minutes or less
    """

    ar_p_model_forecasting()
    print(datetime.datetime.now(), f"forecast_computed")

else:

    pass


