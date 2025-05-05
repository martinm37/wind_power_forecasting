
"""
uploads transformed data into a local MySQL database
"""

import os
import pandas as pd

from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.utils.paths import get_data_file

file_name = "transformed_dataset.csv"
data_df = get_data_file(file_name = file_name)

# making datetime column datetime - converting time column and removing the time offset
data_df["Datetime"] = pd.to_datetime(data_df["Datetime"], utc=True)
data_df["Datetime"] = data_df["Datetime"].dt.tz_convert(None)

# renaming to match names in MySQL db
data_df = data_df.rename(
    columns = {"Datetime" : "datetime",
               "Measured & Upscaled" : "measured_and_upscaled",
               "Monitored capacity" : "monitored_capacity",
               "Rescaled Power" : "rescaled_power"})

# initializing MySQL function wrapper class
connection_dict = {
    "user":os.environ["STANDARD_USER_1"],
    "password":os.environ["STANDARD_USER_1_PASSWORD"],
    "host":"localhost",
    "port":3306,
    "database":"wind_power_db",
    "datatable":"wind_power_transformed_tbl"}

sql_functions_wrapper = SQLFunctionsWrapper(connection_dict = connection_dict)


# checking which datetimes are already present
select_query = ("""
                SELECT datetime
                FROM wind_power_transformed_tbl
                ORDER BY datetime DESC
                """)

query_data = tuple() # an empty tuple of length 0, for compatibility

cnx_object, cursor_object = sql_functions_wrapper.select_query_wrapper(query_text=select_query,query_data=query_data)

already_present_observations = cursor_object.fetchall()

#already_present_observations = select_query_for_datetime_column()

if len(already_present_observations) == 0:
    # there are no data yet, this is the first INSERT:
    # inserting the data
    sql_functions_wrapper.insert_pandas_df_query_wrapper(pandas_df=data_df)
    #pandas_df_insert_query(data_df)

else:

    already_present_observations_df = pd.DataFrame(data=already_present_observations,columns=["datetime"])

    new_set = set(data_df["datetime"])
    present_set = set(already_present_observations_df["datetime"])

    difference_set = new_set - present_set # observation in the new data, that are not in the DB

    difference_df = pd.DataFrame(data=difference_set,columns=["datetime"])
    difference_df["datetime"] = pd.to_datetime(difference_df["datetime"], utc=True)  # converting to time
    difference_df['datetime'] = difference_df['datetime'].dt.tz_convert(None)
    difference_df = difference_df.sort_values(by="datetime", ascending=False)
    difference_df = difference_df.reset_index(drop=True)

    df_to_insert = pd.merge(left=data_df, right=difference_df, on="datetime", how="inner")

    # inserting the data
    sql_functions_wrapper.insert_pandas_df_query_wrapper(pandas_df=df_to_insert)
    #pandas_df_insert_query(df_to_insert)


    #df_to_insert = data_df.join(difference_df, on="datetime", how="inner")
    # this throws error of: ValueError: You are trying to merge on datetime64[ns] and int64 columns for key 'datetime'.
    # -> even though both columns should be datetime64[ns]


