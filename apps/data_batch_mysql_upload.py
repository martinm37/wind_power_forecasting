
"""
uploads transformed data into a local MySQL database
"""

import os
import pandas as pd
from sqlalchemy import create_engine, URL
from sqlalchemy.exc import SQLAlchemyError

from src.utils.paths import get_data_file

file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)

# making datetime column datetime - converting time column and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)

# renaming to match names in MySQL db
data = data.rename(
    columns = {"Datetime" : "datetime",
               "Measured & Upscaled" : "measured_and_upscaled",
               "Monitored capacity" : "monitored_capacity",
               "Rescaled Power" : "rescaled_power"})



#TODO: add here method of obtaining already existing data, and creating only a subset to be inserted

# creating the engine for the connection
url_object = URL.create(
    drivername = "mysql+mysqlconnector",
    username = os.environ["STANDARD_USER_1"],
    password = os.environ["STANDARD_USER_1_PASSWORD"],
    host = "localhost",
    port = 3306,
    database = "wind_power_db")

db_table = "wind_power_transformed_tbl"

engine = create_engine(url_object)

try:
    engine.connect()
    print("connection established successfully")
except SQLAlchemyError as err:
    print(err)
else:
    data.to_sql(name = db_table, con = engine, if_exists="append", index=False)
    print("data upload successful")
