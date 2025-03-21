
import datetime
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMAResults

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

arma_model = ARIMA(endog=rescaled_power_vec,order=(1,0,0))
res = arma_model.fit()
print(res.summary())

print("----------------")

# arma_model_res = ARIMAResults(model = res, )
# aa = arma_model_res.forecast(steps=12)
forecast_vec = res.forecast(steps=96)
print(forecast_vec)


"""
okay so, ARIMAResults is the class of res, i .e. this is what arma_model.fit()
returns
->> and hen forecast method is applied on that it returns the desired forecast, albeit without the 
standard errors

also i do not yet know how to store the parameters, which is necessary at larger ARMA models.

"""






