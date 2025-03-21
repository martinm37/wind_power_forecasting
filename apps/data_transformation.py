
"""
creates the rescaled power vector
"""

import pandas as pd
import os

from src.utils.paths import get_data_file, get_data_path

file_name = "ods031_all_years_2.csv"
data = get_data_file(file_name = file_name)
data_selection = data[["Datetime" ,"Measured & Upscaled" ,"Monitored capacity"]]

# converting time columns
data_selection["Datetime"] = pd.to_datetime(data_selection["Datetime"] ,utc=True)

# removing the time offset
data_selection['Datetime'] = data_selection['Datetime'].dt.tz_convert(None)

data_selection["Rescaled Power"] = data["Measured & Upscaled"] / data["Monitored capacity"] * 100

data_selection.to_csv(os.path.join(get_data_path(),f"transformed_dataset.csv"), sep=",", index=False)


