
"""
forecasting with the AR(p) model
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from src.data_visualization.plotting_functions import forecast_evaluation_plot
from src.statistical_models.ar_model import ar_p_model_comp, ar_p_model_forecast_comp
from src.utils.paths import get_data_file

# data loading
#-------------------

file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)

# converting time columns and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)



# selecting time slice for training
# ---------------------------------
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=1, day=1, hour=0)

data_train = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]

rescaled_power_vec = data_train["Rescaled Power"].to_numpy().reshape(-1,1)


# model fitting
#-------------------
lag_p = 15
ar_p_model_solution = ar_p_model_comp(y_vec = rescaled_power_vec,lag_p = lag_p)


# selecting time slice for forecasting - at least 96 quarters, better do 2 * 96 for a better visualisation
# ------------------------------------------------------

start_day = 4

date_from = datetime.datetime(year=2025, month=3, day=start_day, hour=0)
date_to = datetime.datetime(year=2025, month=3, day=start_day + 3, hour=0)

data_forecast = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]

rescaled_power_vec_forecast = data_forecast["Rescaled Power"].to_numpy().reshape(-1,1)


# forecasting
# ------------------

forecast_init_vec = rescaled_power_vec_forecast[max(96,lag_p) : max(96,lag_p) + len(ar_p_model_solution.beta_vector)-1]
realised_future = rescaled_power_vec_forecast[:96]


forecasted_future = ar_p_model_forecast_comp(starting_y_vec = forecast_init_vec,
                                             beta_vec = ar_p_model_solution.beta_vector,
                                             horizon = 96)

fig = forecast_evaluation_plot(forecast_vec = forecasted_future, realised_vec = np.flip(realised_future),
                               initial_vec = np.flip(rescaled_power_vec_forecast),lag_p=lag_p)
plt.show()

print("eyyoo")