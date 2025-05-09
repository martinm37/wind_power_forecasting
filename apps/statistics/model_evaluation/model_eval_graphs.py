
"""
this file retrieves the forecasted and realized values, and computes various error metrics
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from src.data_visualization.plotting_functions import error_metric_plot, error_metric_plot3
from src.utils.paths import get_model_files_path

lag_p = 48
horizon = 96
test_subset_size = 10000


forecasted_vec_array = np.load(os.path.join(get_model_files_path(),f"forecasted_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))
realized_vec_array = np.load(os.path.join(get_model_files_path(),f"realized_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))

absolute_error_vec_array = np.abs(forecasted_vec_array-realized_vec_array)

MAE_vec = np.sum(absolute_error_vec_array,axis=0) / absolute_error_vec_array.shape[0]

fig = error_metric_plot(metric_vec=MAE_vec,metric_name="Absolute Error",sample_size=test_subset_size,lag_p=lag_p)
plt.show()

print("hello there xdd")






# def mae_p(lag_p):
#     forecasted_vec_array = np.load(
#         os.path.join(get_model_files_path(), f"forecasted_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))
#     realized_vec_array = np.load(
#         os.path.join(get_model_files_path(), f"realized_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"))
#
#     absolute_error_vec_array = np.abs(forecasted_vec_array - realized_vec_array)
#
#     MAE_vec = np.sum(absolute_error_vec_array, axis=0) / absolute_error_vec_array.shape[0]
#
#     return MAE_vec
#
# MAE_vec_15 = mae_p(lag_p = 15)
# MAE_vec_48 = mae_p(lag_p = 48)
# MAE_vec_96 = mae_p(lag_p = 96)
#
# fig = error_metric_plot3(metric_vec1=MAE_vec_15,
#                        metric_vec2=MAE_vec_48,
#                        metric_vec3=MAE_vec_96,
#                        metric_name="Absolute Error",sample_size=1000)
# plt.show()
