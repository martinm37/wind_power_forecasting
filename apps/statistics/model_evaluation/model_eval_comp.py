
"""
this file takes the datetime points of the test subset, and
for each computes forecast, and stores the results along with the realized values
"""

import os
import time
import pickle
import pandas as pd
import numpy as np

from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.utils.paths import get_model_files_path

# TODO:
#  Do a complete rework of the SQL accessing:
#  Create an object containing both initialization and realization vectors, by requesting these from DB _once_,
#  and make the for loop access this, instead of repeatedly accessing DB every time it is run, for every model.
#  This way it can be much more easily reused.

time_start = time.time()

lag_p = 96
horizon = 96
test_subset_size = 5000

print(f"start of evaluating AR({lag_p}) model on subset {test_subset_size}")

connection_dict = {
    "user": os.environ["STANDARD_USER_1"],
    "password": os.environ["STANDARD_USER_1_PASSWORD"],
    "host": "localhost",
    "port": 3306,
    "database": "wind_power_db",
    "datatable": "wind_power_transformed_tbl"}

sql_functions_wrapper = SQLFunctionsWrapper(connection_dict=connection_dict)


# loading pickle file of the trained/fitted model
# ----------------------------------------------
with open(os.path.join(get_model_files_path(),f"ar_p{lag_p}_model_eval_pickle.pkl"),mode='rb') as pkl_file:
    trained_ar_p_model = pickle.load(pkl_file)

# loading the test subset datetimes
# ---------------------------------
datetimes_df = pd.read_pickle(os.path.join(get_model_files_path(),f"test_subset_datetimes_{test_subset_size}.pkl"))


# initializing numpy store arrays

forecasted_vec_array = np.zeros(shape=(test_subset_size,horizon))
realized_vec_array = np.zeros(shape=(test_subset_size,horizon))

t_start_100_iter = time.time()

# start of the for loop
for i in range(test_subset_size):

    datetime_i = datetimes_df["datetimes"].iloc[i]

    # obtaining the init vec

    init_vec_select_query = (f"""
                            SELECT datetime, rescaled_power
                            FROM wind_power_transformed_tbl
                            WHERE datetime < %s 
                            ORDER BY datetime DESC
                            LIMIT {lag_p};
                            """)

    init_vec_select_query_data = (datetime_i,)

    cnx_object, cursor_object = sql_functions_wrapper.select_query_wrapper(query_text=init_vec_select_query,
                                                                           query_data=init_vec_select_query_data)

    data_init = cursor_object.fetchall()
    col_names = cursor_object.column_names
    data_df = pd.DataFrame(data=data_init, columns=col_names)
    forecast_init_vec = data_df["rescaled_power"].to_numpy().reshape(-1, 1)

    # forecasting
    forecast_vec = trained_ar_p_model.model_forecasting(initialization_vector=forecast_init_vec,
                                                        forecast_horizon=horizon)

    # storing
    forecasted_vec_array[i,:] = forecast_vec

    # retrieving realised values

    realized_vec_select_query = (f"""
                                SELECT datetime, rescaled_power
                                FROM wind_power_transformed_tbl
                                WHERE datetime >= %s 
                                ORDER BY datetime ASC
                                LIMIT {horizon};
                                """)

    realized_vec_select_query_data = (datetime_i,)

    cnx_object, cursor_object = sql_functions_wrapper.select_query_wrapper(query_text=realized_vec_select_query,
                                                                           query_data=realized_vec_select_query_data)

    data_realized = cursor_object.fetchall()
    col_names = cursor_object.column_names
    data_df = pd.DataFrame(data=data_realized, columns=col_names)

    # storing
    realized_vec = data_df["rescaled_power"].to_numpy() # for some reason, for the assignment it has to be (96,) and not (96,1)
    realized_vec_array[i,:] = realized_vec

    # logging
    if ( (i+1) % 100 == 0 ):
        t_end_100_iter = time.time()
        elap_time = t_end_100_iter - t_start_100_iter
        print(f"iteration: {i+1}, elapsed time: {round(elap_time, 2)} sec, {round(elap_time / 60, 2)} min")
        t_start_100_iter = time.time()



# exporting

np.save(os.path.join(get_model_files_path(),f"forecasted_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"),
        forecasted_vec_array)

np.save(os.path.join(get_model_files_path(),f"realized_vec_array_{test_subset_size}_ar_p_{lag_p}.npy"),
        realized_vec_array)

time_end = time.time()

print(f"total elapsed time: "
f" {round(time_end - time_start, 2)} sec,"
f" {round((time_end - time_start) / 60, 2)} min")


print("eyyo")





