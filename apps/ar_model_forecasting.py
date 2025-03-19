
"""
forecasting with the AR(p) model
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime

from src.exploratory_statistics.exploratory_statistics import acf_comp, acf_plot
from src.statistical_models.ar_model import ar_p_model_comp, ar_p_model_forecast_comp
from src.utils.paths import get_data_path


def get_data_file(file_name:str):
    data = pd.read_csv(os.path.join(get_data_path(),file_name))
    return data

# data preparation
#-------------------

file_name = "ods031_all_years_2.csv"
data = get_data_file(file_name = file_name)
data_selection = data[["Datetime","Measured & Upscaled","Monitored capacity"]]

# converting time columns
data_selection["Datetime"] = pd.to_datetime(data_selection["Datetime"],utc=True)

# removing the time offset
data_selection['Datetime'] = data_selection['Datetime'].dt.tz_convert(None)

# linear interpolation of the missing values
data_selection["Measured & Upscaled"] = data_selection["Measured & Upscaled"].interpolate(method="linear")

# selecting time slice
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=3, day=1, hour=0)

data_select = data_selection[(data_selection["Datetime"] >= date_from) & (data_selection["Datetime"] < date_to)]

data_matrix = data_select[["Measured & Upscaled","Monitored capacity"]].to_numpy()

#data_selection["Rescaled Power"] = data["Measured & Upscaled"] / data["Monitored capacity"] * 100

print(f"max power: {np.max(data_matrix[:,0])}")
print(f"min power: {np.min(data_matrix[:, 0])}")

truncated_array = np.maximum(data_matrix[:,0],np.zeros(len(data_matrix[:,0]))).reshape(-1,1)
arr_2 = data_matrix[:, 1].reshape(-1,1)
data_matrix_truncated = np.concatenate([truncated_array,arr_2],axis=1)

print(f"max power truncated: {np.max(data_matrix_truncated[:,0])}")
print(f"min power truncated: {np.min(data_matrix_truncated[:, 0])}")

relative_power_vec = (data_matrix_truncated[:,0] / data_matrix_truncated[:,1] * 100).reshape(-1,1)

# separation of the original vector into the training set and forecasting set

relative_power_vec_fit = relative_power_vec[96:]

realised_future = relative_power_vec[:96]

# model fitting
#-------------------

ar_p_model_solution = ar_p_model_comp(y_vec = relative_power_vec_fit,lag_p = 96)

def original_fitted_comparison_plot(original_vec, fitted_vec):

    fig, ax = plt.subplots()

    fig.suptitle(f"original vs fitted vectors")

    axis_vec = np.arange(0,len(original_vec))
    zeros_vec = np.zeros(len(original_vec))

    ax.plot(axis_vec, original_vec)
    ax.plot(axis_vec, fitted_vec)
    ax.plot(axis_vec, zeros_vec, "k--")

    # ax.set_ylabel("partial autocorrelation at lag k")
    # ax.set_xlabel("lag k")

    return fig

# fig = original_fitted_comparison_plot(original_vec = ar_p_model_solution.Y_mat, fitted_vec = ar_p_model_solution.Y_mat_fitted)
# plt.show()


def error_plot(error_vec):

    fig, ax = plt.subplots()

    fig.suptitle(f"errors of the model")

    axis_vec = np.arange(0,len(error_vec))
    zeros_vec = np.zeros(len(error_vec))

    ax.plot(axis_vec, error_vec)
    ax.plot(axis_vec, zeros_vec, "k--")

    # ax.set_ylabel("partial autocorrelation at lag k")
    # ax.set_xlabel("lag k")

    return fig

# fig = error_plot(error_vec = ar_p_model_solution.errors_vector)
# plt.show()


error_acf = acf_comp(y_vec = ar_p_model_solution.errors_vector, total_lag_k = 4*24*5*1)

fig  = acf_plot(acf_vec = error_acf, time_length = len(ar_p_model_solution.errors_vector))
plt.show()



# forecasting

started_vec = relative_power_vec_fit[:len(ar_p_model_solution.beta_vector)-1]

forecasted_future = ar_p_model_forecast_comp(starting_y_vec = started_vec,
                                             beta_vec = ar_p_model_solution.beta_vector,
                                             horizon = 96)


def forecast_evaluation_plot(forecast_vec,realised_vec):

    fig, ax = plt.subplots()

    fig.suptitle(f"Forecasted vs realized values")

    axis_vec = np.arange(0, len(forecast_vec))
    zeros_vec = np.zeros(len(forecast_vec))

    ax.plot(axis_vec, forecast_vec, label = "forecast")
    ax.plot(axis_vec, realised_vec, label = "realization")
    ax.plot(axis_vec, zeros_vec, "k--")
    ax.legend()

    return fig

fig = forecast_evaluation_plot(forecast_vec = forecasted_future, realised_vec = np.flip(realised_future))
plt.show()

print("eyyoo")