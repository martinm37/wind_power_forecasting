
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
from src.utils.paths import get_pickles_path, get_figures_path
from src.utils.utils import adjusted_current_time


def ar_p_model_forecasting():

    # loading pickle file of the trained/fitted model
    # ------------------------------------
    lag_p = 15
    with open(os.path.join(get_pickles_path(),f"ar_p{lag_p}_model_pickle.pkl"),mode='rb') as pkl_file:
        ar_p_model = pickle.load(pkl_file)

    # 'rb' model means "Open the file for reading in binary format.
    # Raises an I/O error if the file does not exist."


    # selecting time slice for forecasting
    # ------------------------------------

    #TODO:
    # 2) somehow make it robust to NULL values, with linear interpolation/extrapolation or smth

    #current_time = datetime.datetime(2025,4,19,13,00)
    current_time = adjusted_current_time()[1]


    data, col_names = select_query_forecast(current_time)
    data_df = pd.DataFrame(data=data, columns=col_names)
    last_day_vec = data_df["rescaled_power"].to_numpy().reshape(-1, 1)
    forecast_init_vec = last_day_vec[:lag_p]

    # forecasting
    # ------------------
    forecast_vec = ar_p_model.model_forecasting(initialization_vector=forecast_init_vec, forecast_horizon=96)

    fig = forecast_plot(forecast_vec,initial_vec=np.flip(last_day_vec.flatten()))
    #plt.show()
    plt.savefig(os.path.join(get_figures_path(),
    f"ar_p_{lag_p}_forecast_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}.png"))

    #print("hello")


if __name__ == "__main__":
    ar_p_model_forecasting()



