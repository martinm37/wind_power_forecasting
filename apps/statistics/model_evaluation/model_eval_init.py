
"""
this script splits the data set into train and test sets,
trains the model on the train set, and selects a subset of the test set, saving the datetime points to a .pkl file
"""

import os
import datetime
import pickle

import pandas as pd
import numpy as np

from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.statistical_models.ar_model import AutoRegressiveModel
from src.utils.paths import get_model_files_path

test_split_datetime = datetime.datetime(2023,1,1,0,0,0)
sample_end_datetime = datetime.datetime(2024,1,1,0,0,0)

lag_p = 192
test_subset_size = 5000



# DB connection
# --------------
connection_dict = {
    "user": os.environ["STANDARD_USER_1"],
    "password": os.environ["STANDARD_USER_1_PASSWORD"],
    "host": "localhost",
    "port": 3306,
    "database": "wind_power_db",
    "datatable": "wind_power_transformed_tbl"}

sql_functions_wrapper = SQLFunctionsWrapper(connection_dict=connection_dict)

# train set
# -------------------------------
train_select_query = ("""
                      SELECT *
                      FROM wind_power_transformed_tbl
                      WHERE datetime < %s
                      ORDER BY datetime DESC;
                      """)

train_select_query_data = (test_split_datetime,)

cnx_object, cursor_object = sql_functions_wrapper.select_query_wrapper(query_text=train_select_query,
                                                                       query_data=train_select_query_data)

train_data = cursor_object.fetchall()
col_names = cursor_object.column_names
train_data_df = pd.DataFrame(data=train_data, columns=col_names)


# model training
# ---------------

ar_p_model = AutoRegressiveModel(lag_order_p=lag_p)

# model fitting
#-------------------
rescaled_power_vec = train_data_df["rescaled_power"].to_numpy().reshape(-1,1)
fitting_solution = ar_p_model.model_fitting(data_vector=rescaled_power_vec)

# exporting to a pickle format
# ----------------------------

with open(os.path.join(get_model_files_path(), f"ar_p{lag_p}_model_eval_pickle.pkl"), mode='wb') as pkl_file:
    pickle.dump(ar_p_model,pkl_file,pickle.HIGHEST_PROTOCOL)


# test set
# --------------------------

test_select_query = ("""
                      SELECT *
                      FROM wind_power_transformed_tbl
                      WHERE datetime >= %s AND datetime < %s
                      ORDER BY datetime DESC;
                      """)

test_select_query_data = (test_split_datetime,sample_end_datetime)

cnx_object, cursor_object = sql_functions_wrapper.select_query_wrapper(query_text=test_select_query,
                                                                       query_data=test_select_query_data)

test_data = cursor_object.fetchall()
col_names = cursor_object.column_names
test_data_df = pd.DataFrame(data=test_data, columns=col_names)

# selecting testing subset
# -------------------------
lag_p_set = int(96*3) # maximal possible, standardizing between models
horizon = 96
test_set_len = len(test_data_df)

test_subset_array = np.arange(start=1+lag_p_set,stop=test_set_len-horizon)

"""
I do not know if np.random.Generator.integers() samples without replacement,
so I will rather use np.random.Generator.choice(), where this option is set explicitly
"""

rng_instance = np.random.default_rng(seed=1375)

random_selection = rng_instance.choice(a=test_subset_array,
                                       size=(test_subset_size,1),
                                       replace=False,
                                       shuffle=False)

random_selection_df = pd.DataFrame(data=random_selection,columns=["int_shifter"])

timedelta_shifters_df = random_selection_df * datetime.timedelta(minutes=15)
timedelta_shifters_df = timedelta_shifters_df.rename(columns = {"int_shifter" : "timedelta_shifter"})

datetimes_df = pd.DataFrame()
datetimes_df["datetimes"] = [test_split_datetime for i in range(test_subset_size)]

datetimes_df["datetimes"] = datetimes_df["datetimes"] + timedelta_shifters_df["timedelta_shifter"]

#exporting
datetimes_df.to_pickle(os.path.join(get_model_files_path(),f"test_subset_datetimes_{test_subset_size}.pkl"))



print("hello")


