
"""
this script runs data_fetch_function(), if the exit state of this function states that full data were
inserted for the current time window, it runs the ar_p_model_forecasting() function on this newest data
"""

import os
import datetime

from apps.data.data_fetcher import data_fetch_function
from apps.statistics.ar_model_forecasting import ar_p_model_forecasting
from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.utils.utils import UpToDateDataTester

# initializing the sql functions wrapper class:
# --------------------------------------------
connection_dict = {
    "user": os.environ["STANDARD_USER_1"],
    "password": os.environ["STANDARD_USER_1_PASSWORD"],
    "host": "localhost",
    "port": 3306,
    "database": "wind_power_db",
    "datatable": "wind_power_transformed_tbl"}

sql_functions_wrapper = SQLFunctionsWrapper(connection_dict=connection_dict)

# fetching newest data
# ----------------------
up_to_date_data_tester = UpToDateDataTester(sql_functions_wrapper)

fetching_exit_status = data_fetch_function(sql_functions_wrapper,up_to_date_data_tester)
print(datetime.datetime.now(),fetching_exit_status)

# forecasting
# ----------------------
if fetching_exit_status == "inserted_full_data":

    """
    this exit state happens only if full data are inserted for the current time window the first time:
    - it should happen only once every 15 minutes or less
    """

    ar_p_model_forecasting(sql_functions_wrapper)
    print(datetime.datetime.now(), f"forecast_computed")

else:

    pass


