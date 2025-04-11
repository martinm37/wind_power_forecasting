
# test script for inserting a whole pandas df into a MySQL DB table

import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

from src.utils.paths import get_data_file

# preparing pandas dataframe
file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)

# converting time columns and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)

truncated_df = data.iloc[600:615,:]
truncated_df = truncated_df.drop("Rescaled Power", axis = 1)


truncated_df = truncated_df.rename(columns = {"Datetime" :"datetime","Measured & Upscaled" :"measured_and_upscaled", "Monitored capacity":"monitored_capacity"})

# creating the engine for the connection
engine = (create_engine(f'mysql+mysqlconnector://{os.environ["TEST_USER_NAME_2"]}:{os.environ["TEST_USER_PASSWORD_2"]}@localhost:3306/test_time_series_db'))

try:
    engine.connect()
    # truncated_df.to_sql("test_time_series_table", con = engine, if_exists="append", index=False)
except SQLAlchemyError as err:
    print(err)
else:
    truncated_df.to_sql("test_time_series_table", con = engine, if_exists="append", index=False)
    print("connection established successfully")

print("xddd")















