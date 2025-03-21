
import datetime
import pandas as pd
import matplotlib.pyplot as plt

from src.exploratory_statistics.statistical_functions import acf_comp, pacf_comp
from src.data_visualization.plotting_functions import acf_plot, pacf_plot
from src.utils.paths import get_data_file

file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)

# converting time columns and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)

print(f'min power: {data["Measured & Upscaled"].min()}')


# selecting time slice
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=3, day=1, hour=0)

# converting to numpy for faster numerical calculation speed
data = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]
data_matrix = data[["Measured & Upscaled", "Monitored capacity","Rescaled Power"]].to_numpy()

rescaled_power_vec = data["Rescaled Power"].to_numpy().reshape(-1,1)

"""
rescaled_power_vec: newest value is on the top
"""

# autocorrelation test statistic

autocorrelation_function_vec = acf_comp(y_vec=rescaled_power_vec, total_lag_k = 4*24*1)
time_length = len(rescaled_power_vec)

fig = acf_plot(autocorrelation_function_vec,time_length)
plt.show()

autocorrelation_function_vec = acf_comp(y_vec=rescaled_power_vec, total_lag_k = 4*24*30*12*5)
time_length = len(rescaled_power_vec)

fig = acf_plot(autocorrelation_function_vec,time_length)
plt.show()

# partial autocorrelation test statistic

pacf_vec = pacf_comp(y_vec = rescaled_power_vec, total_lag_p = 4*24*1)


fig = pacf_plot(pacf_vec = pacf_vec,time_length = len(rescaled_power_vec))
plt.show()



print("hello there xdddd")




