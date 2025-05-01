
"""
training of an AR(p) model
"""

import os
import datetime
import pickle
import pandas as pd
import matplotlib.pyplot as plt

from src.exploratory_statistics.statistical_functions import acf_comp
from src.data_visualization.plotting_functions import acf_plot, original_fitted_comparison_plot, error_plot
from src.mysql_query_functions.mysql_query_functions import select_query_for_whole_data
from src.statistical_models.ar_model import AutoRegressiveModel
from src.utils.paths import get_pickles_path

# data loading
#-------------------
date_start = datetime.datetime(2014,12,31,23,00)
date_end = datetime.datetime(2025,4,28,8,00)

data, col_names = select_query_for_whole_data(date_start,date_end)
data_df = pd.DataFrame(data=data, columns=col_names)

# initialization of the model class
# --------------------------------
lag_p = 15
ar_p_model = AutoRegressiveModel(lag_order_p=lag_p)

# model fitting
#-------------------
rescaled_power_vec = data_df["rescaled_power"].to_numpy().reshape(-1,1)
fitting_solution = ar_p_model.model_fitting(data_vector=rescaled_power_vec)

# exporting to a pickle format
# ----------------------------

with open(os.path.join(get_pickles_path(),f"ar_p{lag_p}_model_pickle.pkl"),mode='wb') as pkl_file:
    pickle.dump(ar_p_model,pkl_file,pickle.HIGHEST_PROTOCOL)

# 'wb' mode means "Open the file for writing in binary format.
# Truncates the file if it already exists.
# Creates a new file if it does not exist."


# model validation
# ------------------
fig = original_fitted_comparison_plot(original_vec = fitting_solution.Y_mat, fitted_vec = fitting_solution.Y_mat_fitted)
plt.show()

fig = error_plot(error_vec = fitting_solution.errors_vector)
plt.show()

error_acf = acf_comp(y_vec = fitting_solution.errors_vector, total_lag_k = 4*24*30*12*10)
fig  = acf_plot(acf_vec = error_acf, time_length = len(fitting_solution.errors_vector))
plt.show()


# print("eyyoo")










