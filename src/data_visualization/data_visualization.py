
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import datetime


from src.utils.paths import get_data_path


def get_data_file(file_name:str):
    data = pd.read_csv(os.path.join(get_data_path(),file_name))
    return data

def wind_series_plotter(time_vec,power_vec,frequency):

    fig, ax = plt.subplots()

    fig.suptitle(f"Wind power time series, {frequency} frequency")

    ax.plot(time_vec,power_vec)
    ax.set_ylabel("power [MW]")
    ax.set_xlabel("time")

    return fig



if __name__ == "__main__":

    #file_name = "ods031_2.csv"
    file_name = "ods031_4_years_2.csv"
    data = get_data_file(file_name = file_name)
    data_selection = data[["Datetime","Measured & Upscaled"]]

    # converting time columns
    data_selection["Datetime"] = pd.to_datetime(data_selection["Datetime"],utc=True)

    # removing the time offset
    data_selection['Datetime'] = data_selection['Datetime'].dt.tz_convert(None)


    # transforming to hourly frequency
    #data_selection_hourly = data_selection.resample(rule = "60min", on = "Datetime").mean()
    data_selection_hourly = data_selection.resample(rule="1h", on="Datetime").mean().reset_index()
    # reset_index() is necessary, otherwise the returned object has just the "Measured & Upscaled" column
    data_selection_hourly[:] = data_selection_hourly.iloc[::-1]
    # the above flips the data, but keeps the index untouched

    # transforming to daily frequency
    data_selection_daily = data_selection.resample(rule="24h", on="Datetime").mean().reset_index()
    data_selection_daily[:] = data_selection_daily.iloc[::-1]

    # transforming to weekly frequency
    data_selection_weekly = data_selection.resample(rule="7d", on="Datetime").mean().reset_index()
    data_selection_weekly[:] = data_selection_weekly.iloc[::-1]

    # transforming to monthly frequency
    data_selection_monthly = data_selection.resample(rule="30d", on="Datetime").mean().reset_index()
    data_selection_monthly[:] = data_selection_monthly.iloc[::-1]


    # day = 2
    # month = 1
    # year = 2025

    # date_from = datetime.datetime(year=year,month=month,day=day,hour=0)
    # date_to = datetime.datetime(year=year,month=month,day=day+1,hour=0)

    date_from = datetime.datetime(year=2021, month=1, day=1, hour=0)
    date_to = datetime.datetime(year=2025, month=3, day=1, hour=0)



    # date_col = data_select["Datetime"]
    # val_col = data_select["Measured & Upscaled"]

    # plotting

    data_select = data_selection[(data_selection["Datetime"] >= date_from) & (data_selection["Datetime"] < date_to)]
    fig = wind_series_plotter(data_select["Datetime"],data_select["Measured & Upscaled"], frequency = "15min")
    plt.show()

    data_select = data_selection_hourly[(data_selection_hourly["Datetime"] >= date_from) & (data_selection_hourly["Datetime"] < date_to)]
    fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="hourly")
    plt.show()

    data_select = data_selection_daily[(data_selection_daily["Datetime"] >= date_from) & (data_selection_daily["Datetime"] < date_to)]
    fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="daily")
    plt.show()

    data_select = data_selection_weekly[(data_selection_weekly["Datetime"] >= date_from) & (data_selection_weekly["Datetime"] < date_to)]
    fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="weekly")
    plt.show()

    data_select = data_selection_monthly[(data_selection_monthly["Datetime"] >= date_from) & (data_selection_monthly["Datetime"] < date_to)]
    fig = wind_series_plotter(data_select["Datetime"], data_select["Measured & Upscaled"], frequency="monthly")
    plt.show()






    print("hello there")










    # plt.plot(date_col,val_col)
    # plt.show()
    # # fig, ax = plt.subplots()
    # # ax.plot(data_day["Datetime"],data_day["Measured & Upscaled"])
    # # plt.plot()


