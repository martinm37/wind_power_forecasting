
import os
import datetime
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import matplotlib.pyplot as plt

from src.exploratory_statistics.statistical_functions import acf_comp, pacf_comp
from src.data_visualization.plotting_functions import acf_plot, pacf_plot
from src.utils.paths import get_data_file

# selecting data from the db
# -------------------------

# selecting time slice
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=3, day=1, hour=0)

try:

    cnx = mysql.connector.connect(user=os.environ["STANDARD_USER_1"],
                                  password=os.environ["STANDARD_USER_1_PASSWORD"],
                                  host="localhost",
                                  port=3306,
                                  database="wind_power_db")

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

    cursor.execute(query, (date_from, date_to))
    fetched_data = cursor.fetchall()
    data = pd.DataFrame(data=fetched_data, columns=cursor.column_names)
    data = data.sort_values(by="datetime", ascending=False)

    # closing the connection to db
    cursor.close()
    cnx.close()

    # start of exploratory statistics
    # -------------------------------

    # renaming to match names in plotting functions
    data = data.rename(
        columns = {"datetime" : "Datetime",
                   "measured_and_upscaled" : "Measured & Upscaled",
                   "monitored_capacity" : "Monitored capacity",
                   "rescaled_power" : "Rescaled Power"})

    # converting to numpy for faster numerical calculation speed
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




