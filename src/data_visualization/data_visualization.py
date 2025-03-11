
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import datetime


from src.utils.paths import get_data_path


def get_data_file(file_name:str):
    data = pd.read_csv(os.path.join(get_data_path(),file_name))
    return data


if __name__ == "__main__":

    file_name = "ods031_2.csv"
    data = get_data_file(file_name = file_name)
    data_selection = data[["Datetime","Measured & Upscaled"]]

    data_selection = data_selection.rename({"Measured & Upscaled":"value"},axis="columns")

    #data_selection["Datetime"] = data_selection["Datetime"].astype('datetime64[ns]')

    data_selection["Datetime"] = pd.to_datetime(data_selection["Datetime"],utc=True)

    # removing the time offset
    data_selection['Datetime'] = data_selection['Datetime'].dt.tz_convert(None)

    day = 2
    month = 1
    year = 2025

    # date_from = datetime.datetime(year=year,month=month,day=day,hour=0)
    # date_to = datetime.datetime(year=year,month=month,day=day+1,hour=0)

    date_from = datetime.datetime(year=2024, month=10, day=20, hour=0)
    date_to = datetime.datetime(year=2024, month=10, day=30, hour=0)

    data_day = data_selection[(data_selection["Datetime"] >= date_from) & (data_selection["Datetime"] < date_to)]

    date_col = data_day["Datetime"]
    val_col = data_day["value"]

    # plotting
    plt.plot(date_col,val_col)
    plt.show()
    # fig, ax = plt.subplots()
    # ax.plot(data_day["Datetime"],data_day["Measured & Upscaled"])
    # plt.plot()



    print("hello there")













