
"""
training of an AR(p) model
"""

import os
import datetime
import pickle
import pandas as pd
import matplotlib.pyplot as plt

from src.exploratory_statistics.statistical_functions import acf_comp
from src.data_visualization.plotting_functions import acf_plot, original_fitted_comparison_plot, error_plot
from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.statistical_models.ar_model import AutoRegressiveModel
from src.utils.paths import get_pickles_path

# data loading
#-------------------

connection_dict = {
    "user": os.environ["STANDARD_USER_1"],
    "password": os.environ["STANDARD_USER_1_PASSWORD"],
    "host": "localhost",
    "port": 3306,
    "database": "wind_power_db",
    "datatable": "wind_power_transformed_tbl"}

sql_functions_wrapper = SQLFunctionsWrapper(connection_dict=connection_dict)

date_start = datetime.datetime(2014,12,31,23,00)
date_end = datetime.datetime(2025,4,28,8,00)

select_query = ("""
                SELECT *
                FROM wind_power_transformed_tbl
                WHERE datetime >= %s AND datetime <= %s
                ORDER BY datetime DESC;
                """)

query_data = (date_start, date_end)

cnx_object, cursor_object = sql_functions_wrapper.select_query_wrapper(query_text=select_query,query_data=query_data)

data = cursor_object.fetchall()
col_names = cursor_object.column_names

#data, col_names = select_query_for_whole_data(date_start,date_end)

data_df = pd.DataFrame(data=data, columns=col_names)

# initialization of the model class
# --------------------------------
lag_p = 96
ar_p_model = AutoRegressiveModel(lag_order_p=lag_p)

# model fitting
#-------------------
rescaled_power_vec = data_df["rescaled_power"].to_numpy().reshape(-1,1)
fitting_solution = ar_p_model.model_fitting(data_vector=rescaled_power_vec)

# exporting to a pickle format
# ----------------------------

with open(os.path.join(get_pickles_path(),f"ar_p{lag_p}_model_pickle.pkl"),mode='wb') as pkl_file:
    pickle.dump(ar_p_model,pkl_file,pickle.HIGHEST_PROTOCOL)

# 'wb' mode means "Open the file for writing in binary format.
# Truncates the file if it already exists.
# Creates a new file if it does not exist."


# model validation
# ------------------
# fig = original_fitted_comparison_plot(original_vec = fitting_solution.Y_mat, fitted_vec = fitting_solution.Y_mat_fitted)
# plt.show()
#
# fig = error_plot(error_vec = fitting_solution.errors_vector)
# plt.show()

# plotting the histogram of errors
plt.hist(rescaled_power_vec,bins=500,color="tab:blue")
plt.xlabel("error")
plt.ylabel("occurrence count")
plt.title(f"distribution of errors from AR({lag_p}) model")
plt.show()


error_acf = acf_comp(y_vec = fitting_solution.errors_vector, total_lag_k = 4*24*30*12*8)
fig  = acf_plot(acf_vec = error_acf, time_length = len(fitting_solution.errors_vector))
plt.show()



# TODO: somehow save figures that are clipped, so that the red lines are separate,
#  right now nothing is properly visible

# print("eyyoo")










