
"""
forecasting with the AR(p) model
"""

import os
import pickle
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.data_visualization.plotting_functions import forecast_plot
from src.mysql_query_functions.mysql_query_functions import select_query_forecast
from src.utils.paths import get_pickles_path


# loading pickle file of the trained/fitted model
# ------------------------------------
lag_p = 15
with open(os.path.join(get_pickles_path(),f"ar_p{lag_p}_model_pickle.pkl"),mode='rb') as pkl_file:
    ar_p_model = pickle.load(pkl_file)

# 'rb' model means "Open the file for reading in binary format.
# Raises an I/O error if the file does not exist."


# selecting time slice for forecasting
# ------------------------------------

current_time = datetime.datetime(2025,4,19,13,00)

data, col_names = select_query_forecast(current_time)
data_df = pd.DataFrame(data=data, columns=col_names)
last_day_vec = data_df["rescaled_power"].to_numpy().reshape(-1, 1)
forecast_init_vec = last_day_vec[:lag_p]

# forecasting
# ------------------
forecast_vec = ar_p_model.model_forecasting(initialization_vector=forecast_init_vec, forecast_horizon=96)

fig = forecast_plot(forecast_vec,initial_vec=np.flip(last_day_vec.flatten()))
plt.show()

print("hello")



