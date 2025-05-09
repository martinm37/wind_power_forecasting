
"""
this file retrieves the forecasted and realized values, and computes various error metrics
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from src.data_visualization.plotting_functions import error_metric_plot, error_metric_plot3
from src.utils.paths import get_model_files_path


def mae_comp(lag_p, test_subset_size):
    forecasted_vec_array = np.load(os.path.join(get_model_files_path(),
                                                f"forecasted_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))
    realized_vec_array = np.load(os.path.join(get_model_files_path(),
                                              f"realized_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))

    if test_subset_size != forecasted_vec_array.shape[0]:
        print("there is size mismatch!")

    absolute_error_vec_array = np.abs(forecasted_vec_array - realized_vec_array)

    mean_absolute_error_vec = np.sum(absolute_error_vec_array, axis=0) / test_subset_size

    return mean_absolute_error_vec


def ae_var_sd_comp(lag_p, test_subset_size):

    forecasted_vec_array = np.load(os.path.join(get_model_files_path(),
                                                f"forecasted_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))

    realized_vec_array = np.load(os.path.join(get_model_files_path(),
                                              f"realized_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))

    if test_subset_size != forecasted_vec_array.shape[0]:
        print("there is size mismatch!")

    absolute_error_vec_array = np.abs(forecasted_vec_array - realized_vec_array)
    mean_absolute_error_vec = np.sum(absolute_error_vec_array, axis=0) / test_subset_size

    absolute_error_variance_vec = (
            np.sum((absolute_error_vec_array - mean_absolute_error_vec) ** 2, axis=0) / (test_subset_size - 1))


    absolute_error_sd_vec = np.sqrt(absolute_error_variance_vec)

    return absolute_error_variance_vec, absolute_error_sd_vec


# single one
# ----------
lag_p = 48
horizon = 96
test_subset_size = 10000


mae_vec = mae_comp(lag_p, test_subset_size)
forecast_sd_vec = ae_var_sd_comp(lag_p, test_subset_size)[1]

fig = error_metric_plot(metric_vec=mae_vec,metric_name="Mean Absolute Error",sample_size=test_subset_size,lag_p=lag_p)
plt.show()

fig = error_metric_plot(metric_vec=forecast_sd_vec,metric_name="Forecast SD",sample_size=test_subset_size,lag_p=lag_p)
plt.show()

# multiple


mae_vec_15 = mae_comp(lag_p = 15, test_subset_size = test_subset_size)
mae_vec_48 = mae_comp(lag_p = 48, test_subset_size = test_subset_size)
mae_vec_96 = mae_comp(lag_p = 96, test_subset_size = test_subset_size)

fig = error_metric_plot3(metric_vec1=mae_vec_15,
                         metric_vec2=mae_vec_48,
                         metric_vec3=mae_vec_96,
                         metric_name="Mean Absolute Error", sample_size=test_subset_size)
plt.show()


forecast_sd_vec_15 = ae_var_sd_comp(lag_p = 15, test_subset_size = test_subset_size)[1]
forecast_sd_vec_48 = ae_var_sd_comp(lag_p = 48, test_subset_size = test_subset_size)[1]
forecast_sd_vec_96 = ae_var_sd_comp(lag_p = 96, test_subset_size = test_subset_size)[1]

fig = error_metric_plot3(metric_vec1=forecast_sd_vec_15,
                         metric_vec2=forecast_sd_vec_48,
                         metric_vec3=forecast_sd_vec_96,
                         metric_name="Forecast SD", sample_size=test_subset_size)
plt.show()



test_subset_size = 5000

mae_vec_96 = mae_comp(lag_p = 96, test_subset_size = test_subset_size)
mae_vec_144 = mae_comp(lag_p = 144, test_subset_size = test_subset_size)
mae_vec_192 = mae_comp(lag_p = 192, test_subset_size = test_subset_size)

fig = error_metric_plot3(metric_vec1=mae_vec_96,
                         metric_vec2=mae_vec_144,
                         metric_vec3=mae_vec_192,
                         metric_name="Mean Absolute Error", sample_size=test_subset_size)
plt.show()

forecast_sd_vec_96 = ae_var_sd_comp(lag_p = 96, test_subset_size = test_subset_size)[1]
forecast_sd_vec_144 = ae_var_sd_comp(lag_p = 144, test_subset_size = test_subset_size)[1]
forecast_sd_vec_192 = ae_var_sd_comp(lag_p = 192, test_subset_size = test_subset_size)[1]

fig = error_metric_plot3(metric_vec1=forecast_sd_vec_96,
                         metric_vec2=forecast_sd_vec_144,
                         metric_vec3=forecast_sd_vec_192,
                         metric_name="Forecast SD", sample_size=test_subset_size)
plt.show()



