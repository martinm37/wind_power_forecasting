
"""
usage of the AR(p) model
"""

import numpy as np
import pandas as pd
import os
import datetime

from src.statistical_models.ar_model import ar_p_model_comp
from src.utils.paths import get_data_path


def get_data_file(file_name:str):
    data = pd.read_csv(os.path.join(get_data_path(),file_name))
    return data

# data preparation

file_name = "ods031_all_years_2.csv"
data = get_data_file(file_name = file_name)
data_selection = data[["Datetime","Measured & Upscaled","Monitored capacity"]]

# converting time columns
data_selection["Datetime"] = pd.to_datetime(data_selection["Datetime"],utc=True)

# removing the time offset
data_selection['Datetime'] = data_selection['Datetime'].dt.tz_convert(None)

# linear interpolation of the missing values
data_selection["Measured & Upscaled"] = data_selection["Measured & Upscaled"].interpolate(method="linear")

# selecting time slice
date_from = datetime.datetime(year=2015, month=1, day=1, hour=0)
date_to = datetime.datetime(year=2025, month=3, day=1, hour=0)

data_select = data_selection[(data_selection["Datetime"] >= date_from) & (data_selection["Datetime"] < date_to)]

data_matrix = data_select[["Measured & Upscaled","Monitored capacity"]].to_numpy()

#data_selection["Rescaled Power"] = data["Measured & Upscaled"] / data["Monitored capacity"] * 100

print(f"max power: {np.max(data_matrix[:,0])}")
print(f"min power: {np.min(data_matrix[:, 0])}")

truncated_array = np.maximum(data_matrix[:,0],np.zeros(len(data_matrix[:,0]))).reshape(-1,1)
arr_2 = data_matrix[:, 1].reshape(-1,1)
data_matrix_truncated = np.concatenate([truncated_array,arr_2],axis=1)

print(f"max power truncated: {np.max(data_matrix_truncated[:,0])}")
print(f"min power truncated: {np.min(data_matrix_truncated[:, 0])}")

relative_power_vec = (data_matrix_truncated[:,0] / data_matrix_truncated[:,1] * 100).reshape(-1,1)

# model fitting

ar_p_model_solution = ar_p_model_comp(y_vec = relative_power_vec,lag_p = 12)



print("eyyoo")










