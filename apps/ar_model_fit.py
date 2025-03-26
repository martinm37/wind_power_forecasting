
"""
usage of the AR(p) model
"""

import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



from src.exploratory_statistics.statistical_functions import acf_comp
from src.data_visualization.plotting_functions import acf_plot, original_fitted_comparison_plot, error_plot
from src.statistical_models.ar_model import ar_p_model_comp, ar_p_model_forecast_comp
from src.utils.paths import get_data_path, get_data_file

# data loading
#-------------------

file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)

# converting time columns and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)

print(f'min power: {data["Measured & Upscaled"].min()}')


# selecting time slice for training
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=3, day=1, hour=0)

data = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]

rescaled_power_vec = data["Rescaled Power"].to_numpy().reshape(-1,1)

# model fitting
#-------------------
ar_p_model_solution = ar_p_model_comp(y_vec = rescaled_power_vec,lag_p = 5)


# model validation
# ------------------

fig = original_fitted_comparison_plot(original_vec = ar_p_model_solution.Y_mat, fitted_vec = ar_p_model_solution.Y_mat_fitted)
plt.show()


fig = error_plot(error_vec = ar_p_model_solution.errors_vector)
plt.show()


error_acf = acf_comp(y_vec = ar_p_model_solution.errors_vector, total_lag_k = 4*24*30*12*10)

fig  = acf_plot(acf_vec = error_acf, time_length = len(ar_p_model_solution.errors_vector))
plt.show()




# print("eyyoo")










