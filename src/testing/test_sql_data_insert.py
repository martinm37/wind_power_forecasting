
# script for testing the insertion of specific rows into the MySQL Databse

import os
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import datetime

from src.utils.paths import get_data_file

# preparing data
file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)

# converting time columns and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)

col = 320

test_datetime = data.iloc[col,0]
test_m_n_u = data.iloc[col,1]
test_m_c = data.iloc[col,2]


# inserting data

try:
    cnx = mysql.connector.connect(user=os.environ["TEST_USER_NAME_2"],
                                  password=os.environ["TEST_USER_PASSWORD_2"],
                                  host = "localhost",
                                  database = "test_time_series_db")

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

else:
    cursor = cnx.cursor()

    insert_query = ("""
                    INSERT INTO test_time_series_table
                    (datetime, measured_and_upscaled, monitored_capacity)
                    VALUES
                    (%s, %s, %s);
                    """)

    query_data = (test_datetime,test_m_n_u,test_m_c)

    # inserting new data into the DB
    cursor.execute(insert_query,query_data)

    # commiting
    cnx.commit()

    # exiting
    cursor.close()
    cnx.close()
