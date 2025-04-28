
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMAResults

from src.data_visualization.plotting_functions import forecast_evaluation_plot, forecast_comparison_plot
from src.statistical_models.ar_model import ar_p_model_forecast_comp, ar_p_model_comp
from src.utils.paths import get_data_file

# data loading
#-------------------

file_name = "transformed_dataset.csv"
data = get_data_file(file_name = file_name)

# converting time columns and removing the time offset
data["Datetime"] = pd.to_datetime(data["Datetime"] ,utc=True)
data["Datetime"] = data["Datetime"].dt.tz_convert(None)



# selecting time slice for training
# ---------------------------------
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=1, day=1, hour=0)

data_train = data[(data["Datetime"] >= date_from) & (data["Datetime"] < date_to)]

rescaled_power_vec = data_train["Rescaled Power"].to_numpy().reshape(-1,1)


# model fitting
#-------------------

lag_p = 15


arma_model = ARIMA(endog=rescaled_power_vec,order=(lag_p,0,0))
# arma_model = ARIMA(endog=rescaled_power_vec,order=(1,0,0),seasonal_order=(0,1,0,35064)) # - this uses all ram and swap xd
res = arma_model.fit()
print(res.summary())

print("----------------")

# arma_model_res = ARIMAResults(model = res, )
# aa = arma_model_res.forecast(steps=12)
forecast_vec = res.forecast(steps=96)
#print(forecast_vec)


"""
okay so, ARIMAResults is the class of res, i .e. this is what arma_model.fit()
returns
->> and hen forecast method is applied on that it returns the desired forecast, albeit without the 
standard errors

also i do not yet know how to store the parameters, which is necessary at larger ARMA models.

"""

# comparison part

# model fitting
#-------------------

ar_p_model_solution = ar_p_model_comp(y_vec = rescaled_power_vec,lag_p = lag_p)

print(ar_p_model_solution.beta_vector)


# selecting time slice for forecasting - at least 96 quarters, better do 2 * 96 for a better visualisation
# ------------------------------------------------------

start_day = 1

date_from_forecast = datetime.datetime(year=2025, month=1, day=start_day, hour=0)
date_to_forecast = datetime.datetime(year=2025, month=1, day=start_day + 1, hour=0)

data_forecast = data[(data["Datetime"] >= date_from_forecast) & (data["Datetime"] < date_to_forecast)]

rescaled_power_vec_forecast = data_forecast["Rescaled Power"].to_numpy().reshape(-1,1)


# forecasting
# ------------------

forecast_init_vec = rescaled_power_vec[0 : lag_p]
realised_future_f = rescaled_power_vec_forecast


forecasted_future = ar_p_model_forecast_comp(starting_y_vec = forecast_init_vec,
                                             beta_vec = ar_p_model_solution.beta_vector,
                                             horizon = 96)

difference_vector = forecasted_future - forecast_vec

fig = forecast_comparison_plot(forecast_vec_1 = forecasted_future,
                               forecast_vec_2 = forecast_vec,
                               realised_vec = np.flip(realised_future_f),
                               initial_vec = np.flip(rescaled_power_vec),lag_p=lag_p)
plt.show()




