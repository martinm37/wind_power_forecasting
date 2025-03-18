
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

def acf_comp(y_vec, total_lag_k):
    """
    computes the autocorrelation function
    y_vec: T x 1 vector of a time series data - *** first value has to be the newest one !!!! ***
    total_lag_k: for how many lags we want to compute acf

    returns acf_vec: total_lag_k x 1 vector of autocorrelations
    """

    time_length = len(y_vec)

    y_mean = np.sum(y_vec) / time_length

    y_vec_demeaned = y_vec - y_mean

    y_variance = y_vec_demeaned.T @ y_vec_demeaned  # WITHOUT dividing - as it cancels out later on

    acf_vec = np.zeros(total_lag_k).reshape(-1, 1)

    for i in range(len(acf_vec)):
        first_vec = y_vec_demeaned[0:time_length - i - 1]  # from 1 to T - i
        second_vec = y_vec_demeaned[i + 1:]  # from i to T

        acf_vec[i] = first_vec.T @ second_vec / y_variance

    return acf_vec


def acf_plot(acf_vec,time_length):

    lag_vec = np.arange(1, len(acf_vec) + 1)
    zeros_vec = np.zeros(len(acf_vec))

    sig_val = 1.96 * 1 / np.sqrt(time_length)

    #print(sig_val)
    # top_sig_vec = np.ones(len(acf_vec)) * 1.96 / 10
    # bottom_sig_vec = np.ones(len(acf_vec)) * -1.96 / 10

    top_sig_vec = np.ones(len(acf_vec)) * sig_val
    bottom_sig_vec = np.ones(len(acf_vec)) * -sig_val

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


def pacf_plot(pacf_vec,time_length):

    lag_vec = np.arange(1, len(pacf_vec) + 1)
    zeros_vec = np.zeros(len(pacf_vec))

    sig_val = 1.96 * 1 / np.sqrt(time_length)

    #print(sig_val)
    # top_sig_vec = np.ones(len(acf_vec)) * 1.96 / 10
    # bottom_sig_vec = np.ones(len(acf_vec)) * -1.96 / 10

    top_sig_vec = np.ones(len(pacf_vec)) * sig_val
    bottom_sig_vec = np.ones(len(pacf_vec)) * -sig_val

    fig, ax = plt.subplots()

    fig.suptitle(f"Partial autocorrelation function, N = {time_length}")

    ax.plot(lag_vec, pacf_vec)
    ax.plot(lag_vec, zeros_vec, "k--")
    ax.plot(lag_vec, top_sig_vec, "r--")
    ax.plot(lag_vec, bottom_sig_vec, "r--")
    ax.set_yticks(np.arange(-0.5, 1.1, step=0.1))

    ax.set_ylabel("partial autocorrelation at lag k")
    ax.set_xlabel("lag k")

    return fig


def pacf_ar_p_fit(y_vec,lag_p):

    """
    computes the AR(p) model for the purposes of computation of
    partial autoccorelation function
    ---> does not include an intercept in the model equation

    original vector y_vec has dimensions of T x 1
    new vectors will have dimensions (T - lag_p) x 1
    """
    time_length = len(y_vec)

    Y_mat = y_vec[0:time_length - lag_p]

    X_mat = np.zeros((time_length - lag_p,lag_p))

    for i in range(0,lag_p):
        i_indx = i + 1 # easier for indexing
        #print(f"{i_indx},{time_length - lag_p + i_indx}")
        selection = y_vec[i_indx : time_length - lag_p + i_indx , 0]
        X_mat[:,i] = selection

    # OLS estimation
    beta_vec = np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T @ Y_mat

    return beta_vec


def pacf_comp(y_vec,total_lag_p):

    """
    computes the partial autocorrelation function
    """

    time_length = len(y_vec)

    y_mean = np.sum(y_vec) / time_length

    y_vec_demeaned = y_vec - y_mean

    pacf_vec = np.zeros(total_lag_p).reshape(-1, 1)

    for i in range(len(pacf_vec)):
        print(f"computing lag {i+1} of {len(pacf_vec)}")

        beta_vec_i = pacf_ar_p_fit(y_vec = y_vec_demeaned,lag_p = i+1) # lag starts from 1

        pacf_vec[i] = beta_vec_i[-1]

    return pacf_vec


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



    #autocorrelation_function_vec = acf_comp(y_vec = relative_power_vec, total_lag_k = 4*24*30*12)
    autocorrelation_function_vec = acf_comp(y_vec=relative_power_vec, total_lag_k = 4*24*1)

    time_length = len(relative_power_vec)

    fig = acf_plot(autocorrelation_function_vec,time_length)
    plt.show()


    #pacf_vec_test = pacf_ar_p_fit(y_vec = relative_power_vec,lag_p = 4)
    pacf_vec_test = pacf_comp(y_vec = relative_power_vec, total_lag_p = 4*24*1)


    fig = pacf_plot(pacf_vec = pacf_vec_test,time_length = len(relative_power_vec))
    plt.show()


    print("eyyoo xdddd")




 # #  *** top value is the newest ***
 #
 #    time_length = len(relative_power_vec)
 #
 #    mean_value = np.sum(relative_power_vec) / time_length
 #
 #    relative_power_demeaned_vec = relative_power_vec - mean_value
 #
 #    #relative_power_variance = (1/(time_length-1)) * relative_power_demeaned_vec.T @ relative_power_demeaned_vec
 #    relative_power_variance = relative_power_demeaned_vec.T @ relative_power_demeaned_vec # WITHOUT dividing
 #
 #
 #    measurement_span = 4*24*30*12*4
 #
 #    autocorrelation_function_vec = np.zeros(measurement_span).reshape(-1,1)
 #
 #    for i in range(len(autocorrelation_function_vec)):
 #        first_vec = relative_power_demeaned_vec[0:time_length-i-1] # from 1 to T - i
 #        second_vec = relative_power_demeaned_vec[i+1:]             # from i to T
 #
 #        autocorrelation_function_vec[i] = first_vec.T @ second_vec / relative_power_variance





