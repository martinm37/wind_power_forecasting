
"""
training of arima type models through statsmodels package
"""


import os
import datetime
import pickle
import time
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

from src.data_visualization.plotting_functions import acf_plot
from src.exploratory_statistics.statistical_functions import acf_comp
from src.mysql_query_functions.mysql_query_functions import SQLFunctionsWrapper
from src.utils.paths import get_model_files_path, get_figures_path

time_start = time.time()

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

print("database connection established")

data = cursor_object.fetchall()
col_names = cursor_object.column_names

#data, col_names = select_query_for_whole_data(date_start,date_end)

data_df = pd.DataFrame(data=data, columns=col_names)

rescaled_power_vec = data_df["rescaled_power"].to_numpy().reshape(-1,1)

print("data loaded")

# model fitting
#-------------------

lag_p = 12
lag_d = 0
lag_q = 12


arma_model = ARIMA(endog=rescaled_power_vec,order=(lag_p,lag_d,lag_q))
arma_model_trained = arma_model.fit()
print(arma_model_trained.summary())

# exporting to a pickle format
# ----------------------------

with open(os.path.join(get_model_files_path(), f"arma_p{lag_p}_d{lag_d}_q{lag_q}_model_pickle.pkl"), mode='wb') as pkl_file:
    pickle.dump(arma_model_trained,pkl_file,pickle.HIGHEST_PROTOCOL)

"""
the pickle files of these models are absurdly large, (15,0,15) model had a pickle file of 12GB
-> last model without errors was (12,0,12)
"""

print("model class trained and pickled")

# computing error acf
# -------------------
error_vector = rescaled_power_vec - arma_model_trained.fittedvalues.reshape(-1,1)

error_acf = acf_comp(y_vec = error_vector, total_lag_k = 4*24*30*12*5)

time_end = time.time()

fig  = acf_plot(acf_vec = error_acf, time_length = len(error_vector))
plt.show()
# plt.savefig(os.path.join(get_figures_path(),f"arma_p{lag_p}_d{lag_d}_q{lag_q}_model_error_acf.svg"))

print(f"total elapsed time: "
f" {round(time_end - time_start, 2)} sec,"
f" {round((time_end - time_start) / 60, 2)} min")


# print("----------------")
#
# # arma_model_res = ARIMAResults(model = res, )
# # aa = arma_model_res.forecast(steps=12)
# forecast_vec = res.forecast(steps=96)
# #print(forecast_vec)
#
#
# """
# okay so, ARIMAResults is the class of res, i .e. this is what arma_model.fit()
# returns
# ->> and hen forecast method is applied on that it returns the desired forecast, albeit without the
# standard errors
#
# also i do not yet know how to store the parameters, which is necessary at larger ARMA models.
#
# """
#
# # comparison part
#
# # model fitting
# #-------------------
#
# ar_p_model_solution = ar_p_model_comp(y_vec = rescaled_power_vec,lag_p = lag_p)
#
# print(ar_p_model_solution.beta_vector)
#
#
# # selecting time slice for forecasting - at least 96 quarters, better do 2 * 96 for a better visualisation
# # ------------------------------------------------------
#
# start_day = 1
#
# date_from_forecast = datetime.datetime(year=2025, month=1, day=start_day, hour=0)
# date_to_forecast = datetime.datetime(year=2025, month=1, day=start_day + 1, hour=0)
#
# data_forecast = data[(data["Datetime"] >= date_from_forecast) & (data["Datetime"] < date_to_forecast)]
#
# rescaled_power_vec_forecast = data_forecast["Rescaled Power"].to_numpy().reshape(-1,1)
#
#
# # forecasting
# # ------------------
#
# forecast_init_vec = rescaled_power_vec[0 : lag_p]
# realised_future_f = rescaled_power_vec_forecast
#
#
# forecasted_future = ar_p_model_forecast_comp(starting_y_vec = forecast_init_vec,
#                                              beta_vec = ar_p_model_solution.beta_vector,
#                                              horizon = 96)
#
# difference_vector = forecasted_future - forecast_vec
#
# fig = forecast_comparison_plot(forecast_vec_1 = forecasted_future,
#                                forecast_vec_2 = forecast_vec,
#                                realised_vec = np.flip(realised_future_f),
#                                initial_vec = np.flip(rescaled_power_vec),lag_p=lag_p)
# plt.show()
#

# arma_model = ARIMA(endog=rescaled_power_vec,order=(1,0,0),seasonal_order=(0,1,0,35064)) # - this uses all ram and swap xd




