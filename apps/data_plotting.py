

import matplotlib.pyplot as plt
import datetime
import pandas as pd

from src.data_visualization.data_visualization import wind_series_plotter, wind_series_plotter_rescaled, \
    wind_series_plotter_with_capacity
from src.utils.paths import get_data_file

file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)


# converting time columns and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)

# selecting plotting window
# --------------------------
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=3, day=1, hour=0)

# time transformations and plotting
# ----------------------------------

# transforming to hourly frequency
# data_selection_hourly = data_selection.resample(rule = "60min", on = "Datetime").mean()
data_hourly = data.resample(rule="1h", on="Datetime").mean().reset_index()
# reset_index() is necessary, otherwise the returned object has just the "Measured & Upscaled" column
data_hourly[:] = data_hourly.iloc[::-1]
# the above flips the data, but keeps the index untouched

# transforming to daily frequency
data_daily = data.resample(rule="24h", on="Datetime").mean().reset_index()
data_daily[:] = data_daily.iloc[::-1]

# transforming to weekly frequency
data_weekly = data.resample(rule="7d", on="Datetime").mean().reset_index()
data_weekly[:] = data_weekly.iloc[::-1]

# transforming to monthly frequency
data_monthly = data.resample(rule="30d", on="Datetime").mean().reset_index()
data_monthly[:] = data_monthly.iloc[::-1]

# transforming to quarterly frequency
data_quarterly = data.resample(rule="120d", on="Datetime").mean().reset_index()
data_quarterly[:] = data_quarterly.iloc[::-1]

# transforming to half yearly frequency
data_half_yearly = data.resample(rule="180d", on="Datetime").mean().reset_index()
data_half_yearly[:] = data_half_yearly.iloc[::-1]


# plotting - original series, different time aggregation
# ----------------------

# data_select = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]
# fig = wind_series_plotter(data_select["Datetime"],data_select["Measured & Upscaled"], frequency = "15min")
# plt.show()
#
# data_select = data_hourly[(data_hourly["Datetime"] >= date_from) & (data_hourly["Datetime"] < date_to)]
# fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="hourly")
# plt.show()
#
# data_select = data_daily[(data_daily["Datetime"] >= date_from) & (data_daily["Datetime"] < date_to)]
# fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="daily")
# plt.show()

# data_select = data_weekly[(data_weekly["Datetime"] >= date_from) & (data_weekly["Datetime"] < date_to)]
# fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="weekly")
# plt.show()
#
# data_select = data_monthly[(data_monthly["Datetime"] >= date_from) & (data_monthly["Datetime"] < date_to)]
# fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="monthly")
# plt.show()
#
# data_select = data_quarterly[(data_quarterly["Datetime"] >= date_from) & (data_quarterly["Datetime"] < date_to)]
# fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="quarterly")
# plt.show()
#
# data_select = data_half_yearly[(data_half_yearly["Datetime"] >= date_from) & (data_half_yearly["Datetime"] < date_to)]
# fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="half yearly")
# plt.show()


# plotting - original series, with capacity
# ----------------------

# data_select = data_monthly[(data_monthly["Datetime"] >= date_from) & (data_monthly["Datetime"] < date_to)]
# fig = wind_series_plotter_with_capacity(data_select["Datetime"], data_select["Measured & Upscaled"],
#                                         data_select["Monitored capacity"], frequency="monthly")
# plt.show()
#
# fig = wind_series_plotter_with_capacity(data_select["Datetime"], data_select["Measured & Upscaled"],
#                                         data_select["Monitored capacity"], frequency="quarterly")
# plt.show()



# plotting - rescaled series
# ----------------------

# data_select = data_weekly[(data_weekly["Datetime"] >= date_from) & (data_weekly["Datetime"] < date_to)]
# fig = wind_series_plotter_rescaled(data_select["Datetime"], data_select["Rescaled Power"], frequency="weekly")
# plt.show()
#
# data_select = data_monthly[(data_monthly["Datetime"] >= date_from) & (data_monthly["Datetime"] < date_to)]
# fig = wind_series_plotter_rescaled(data_select["Datetime"], data_select["Rescaled Power"], frequency="monthly")
# plt.show()
#
# data_select = data_quarterly[(data_quarterly["Datetime"] >= date_from) & (data_quarterly["Datetime"] < date_to)]
# fig = wind_series_plotter_rescaled(data_select["Datetime"], data_select["Rescaled Power"], frequency="quarterly")
# plt.show()
#
# data_select = data_half_yearly[(data_half_yearly["Datetime"] >= date_from) & (data_half_yearly["Datetime"] < date_to)]
# fig = wind_series_plotter_rescaled(data_select["Datetime"], data_select["Rescaled Power"], frequency="half yearly")
# plt.show()





