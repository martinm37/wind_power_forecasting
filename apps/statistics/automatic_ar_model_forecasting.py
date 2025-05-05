
"""
this script runs data_fetch_function(), if the exit state of this function states that full data were
inserted for the current time window, it runs the ar_p_model_forecasting() function on this newest data
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

from apps.data.data_fetcher import data_fetch_function
from apps.statistics.ar_model_forecasting import ar_p_model_forecasting
from src.data_visualization.plotting_functions import forecast_plot, forecast_plot_three_models
from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.utils.paths import get_figures_path
from src.utils.utils import UpToDateDataTester, adjusted_current_time

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


    # for a single model:
    #-------------------
    # lag_p = 15
    # forecast_vec_p_15, last_day_vec = ar_p_model_forecasting(sql_functions_wrapper, lag_p=lag_p)
    # current_time = adjusted_current_time()[1]
    #
    # fig = forecast_plot(forecast_vec_p_15, initial_vec=np.flip(last_day_vec.flatten()))
    # # plt.show()
    # plt.savefig(os.path.join(get_figures_path(),
    # f"ar_p_{lag_p}_forecast_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}.svg"))

    # comparison of three models:
    # ---------------------------
    forecast_vec_15, last_day_vec = ar_p_model_forecasting(sql_functions_wrapper,lag_p=15)
    forecast_vec_48 = ar_p_model_forecasting(sql_functions_wrapper,lag_p=48)[0]
    forecast_vec_96 = ar_p_model_forecasting(sql_functions_wrapper,lag_p=96)[0]

    current_time = adjusted_current_time()[1]

    fig = forecast_plot_three_models(forecast_vec_15,forecast_vec_48,forecast_vec_96,initial_vec=np.flip(last_day_vec.flatten()))
    #plt.show()
    plt.savefig(os.path.join(get_figures_path(),
    f"three_ar_p_forecasts_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}.svg"))


    print(datetime.datetime.now(), f"forecast_computed")

else:

    pass


