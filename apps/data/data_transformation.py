
"""
transforms historical wind power production data obtained from a .csv file
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from src.utils.paths import get_data_file, get_data_path

file_name = "ods031_edit.csv"
data = get_data_file(file_name = file_name)
data_selection = data[["Datetime" ,"Measured & Upscaled" ,"Monitored capacity"]]

# work on the time column
data_selection["Datetime"] = pd.to_datetime(data_selection["Datetime"] ,utc=True) # converting to time
data_selection['Datetime'] = data_selection['Datetime'].dt.tz_convert(None) # removing the time offset

# removing NaT (Not a Time) observations
# two functions: .isnull and .notnull -> same just different True/False values
non_null_rows = pd.notnull(data['Datetime']) # True: normal time, False: NaT
data_selection = data_selection.loc[non_null_rows]

# linear interpolation of the missing values
data_selection["Measured & Upscaled"] = data_selection["Measured & Upscaled"].interpolate(method="linear")

# lower bounding the power vector at 0
print(f'min power: {data_selection["Measured & Upscaled"].min()}')

power_vec = data_selection["Measured & Upscaled"].to_numpy()
power_vec_bounded = np.maximum(power_vec,np.zeros(len(power_vec))) #.reshape(-1,1)

# creating the vector of relative power
capacity_vec = data_selection["Monitored capacity"].to_numpy()
rescaled_power_vec = power_vec / capacity_vec * 100

plt.hist(rescaled_power_vec,bins=500,color="tab:blue")
# plt.xlabel("error")
# plt.ylabel("occurrence count")
# plt.title(f"distribution of errors from AR({lag_p}) model")
plt.show()

# bounding relative power vector - there are values below 0 and above 100
rescaled_power_vec_lower_bounded = np.maximum(rescaled_power_vec,np.zeros(len(power_vec))) #.reshape(-1,1)
rescaled_power_vec_bounded = np.minimum(rescaled_power_vec_lower_bounded,np.ones(len(power_vec))*100)

# storing in the data frame
data_selection["Measured & Upscaled"] = pd.Series(power_vec_bounded)
data_selection["Rescaled Power"] = pd.Series(rescaled_power_vec_bounded)
print(f'min power: {data_selection["Measured & Upscaled"].min()}')


data_selection.to_csv(os.path.join(get_data_path(),f"transformed_dataset.csv"), sep=",", index=False)




