
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import datetime


from src.utils.paths import get_data_path


def get_data_file(file_name:str):
    data = pd.read_csv(os.path.join(get_data_path(),file_name))
    return data


def wind_series_plotter_rescaled(time_vec,power_vec,frequency):

    fig, ax = plt.subplots()

    fig.suptitle(f"Wind power time series, rescaled, {frequency} frequency")

    ax.plot(time_vec,power_vec)
    ax.set_ylabel("power [% of total capacity]")
    ax.set_xlabel("time")

    return fig

def acf_plot(acf_vec,time_length):

    lag_vec = np.arange(1, len(acf_vec) + 1)
    zeros_vec = np.zeros(len(acf_vec))
    sig_val = 1.96 / np.sqrt(time_length)
    print(sig_val)

    top_sig_vec = np.ones(len(acf_vec)) * 1.96 / 10
    bottom_sig_vec = np.ones(len(acf_vec)) * -1.96 / 10

    fig, ax = plt.subplots()

    fig.suptitle(f"Autocorrelation function, N = {time_length}")

    ax.plot(lag_vec, acf_vec)
    ax.plot(lag_vec, zeros_vec, "k--")
    ax.plot(lag_vec, top_sig_vec, "r--")
    ax.plot(lag_vec, bottom_sig_vec, "r--")
    ax.set_yticks(np.arange(-0.5, 1.1, step=0.1))

    ax.set_ylabel("autocorrelation at lag k")
    ax.set_xlabel("lag k")

    return fig


if __name__ == "__main__":


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

    #  *** top value is the newest ***

    time_length = len(relative_power_vec)

    mean_value = np.sum(relative_power_vec) / time_length

    relative_power_demeaned_vec = relative_power_vec - mean_value

    #relative_power_variance = (1/(time_length-1)) * relative_power_demeaned_vec.T @ relative_power_demeaned_vec
    relative_power_variance = relative_power_demeaned_vec.T @ relative_power_demeaned_vec # WITHOUT dividing


    measurement_span = 4*24*30

    autocorrelation_function_vec = np.zeros(measurement_span).reshape(-1,1)

    for i in range(len(autocorrelation_function_vec)):
        first_vec = relative_power_demeaned_vec[0:time_length-i-1] # from 1 to T - i
        second_vec = relative_power_demeaned_vec[i+1:]             # from i to T

        autocorrelation_function_vec[i] = first_vec.T @ second_vec / relative_power_variance


    fig = acf_plot(autocorrelation_function_vec,time_length)

    plt.show()



    print("eyyoo xdddd")





