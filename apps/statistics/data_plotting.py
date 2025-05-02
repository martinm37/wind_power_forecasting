
"""
script for various types of plots for the selected time window
"""

import os
import datetime
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import matplotlib.pyplot as plt

from src.data_visualization.data_visualization import wind_series_plotter, wind_series_plotter_rescaled, \
    wind_series_plotter_with_capacity
from src.utils.paths import get_data_file


# selecting plotting window
# --------------------------
date_from = datetime.datetime(year=2025, month=2, day=15, hour=0)
date_to = datetime.datetime(year=2025, month=2, day=28, hour=0)

# obtaining data from db
# --------------------------
try:

    cnx = mysql.connector.connect(user=os.environ["STANDARD_USER_1"],
                                  password=os.environ["STANDARD_USER_1_PASSWORD"],
                                  host = "localhost",
                                  port = 3306,
                                  database = "wind_power_db")

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

else:

    cursor = cnx.cursor()

    query = ("""
            SELECT * 
            FROM wind_power_transformed_tbl
            WHERE datetime >= %s AND datetime < %s;
            """)

    cursor.execute(query,(date_from,date_to))
    fetched_data = cursor.fetchall()
    data = pd.DataFrame(data = fetched_data, columns = cursor.column_names)

    # closing the connection to db
    cursor.close()
    cnx.close()


    # start of plotting section
    # --------------------------

    data = data.sort_values(by="datetime",ascending=False)

    # renaming to match names in plotting functions
    data = data.rename(
        columns = {"datetime" : "Datetime",
                   "measured_and_upscaled" : "Measured & Upscaled",
                   "monitored_capacity" : "Monitored capacity",
                   "rescaled_power" : "Rescaled Power"})



    # # converting time columns and removing the time offset
    # data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
    # data["Datetime"] = data["Datetime"].dt.tz_convert(None)
    #
    # # selecting plotting window
    # # --------------------------
    # date_from = datetime.datetime(year=2025, month=2, day=1, hour=0)
    # date_to = datetime.datetime(year=2025, month=3, day=10, hour=0)

    # time transformations and plotting
    # ----------------------------------

    # transforming to hourly frequency
    # data_selection_hourly = data_selection.resample(rule = "60min", on = "Datetime").mean()
    data_hourly = data.resample(rule="1h", on="Datetime").mean().reset_index()
    # reset_index() is necessary, otherwise the returned object has just the "Measured & Upscaled" column
    data_hourly = data_hourly.sort_values(by="Datetime", ascending=False)

    # transforming to daily frequency
    data_daily = data.resample(rule="24h", on="Datetime").mean().reset_index()
    data_daily = data_daily.sort_values(by="Datetime", ascending=False)

    # transforming to weekly frequency
    data_weekly = data.resample(rule="7d", on="Datetime").mean().reset_index()
    data_weekly = data_weekly.sort_values(by="Datetime", ascending=False)

    # transforming to monthly frequency
    data_monthly = data.resample(rule="30d", on="Datetime").mean().reset_index()
    data_monthly = data_monthly.sort_values(by="Datetime", ascending=False)

    # transforming to quarterly frequency
    data_quarterly = data.resample(rule="120d", on="Datetime").mean().reset_index()
    data_quarterly = data_quarterly.sort_values(by="Datetime", ascending=False)

    # transforming to half yearly frequency
    data_half_yearly = data.resample(rule="180d", on="Datetime").mean().reset_index()
    data_half_yearly = data_half_yearly.sort_values(by="Datetime", ascending=False)


    # plotting - original series, different time aggregation
    # ----------------------

    # data_select = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]
    # fig = wind_series_plotter(data_select["Datetime"],data_select["Measured & Upscaled"], frequency = "15min")
    # plt.show()

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

    data_select = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]
    fig = wind_series_plotter(data_select["Datetime"],data_select["Rescaled Power"], frequency = "15min")
    plt.show()

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





