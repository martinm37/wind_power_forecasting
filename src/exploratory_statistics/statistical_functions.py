
import numpy as np
import pandas as pd
import datetime
import time


from src.utils.paths import get_data_file


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

    t0 = time.time()

    time_length = len(y_vec)

    #y_mean = np.sum(y_vec) / time_length
    #y_vec_demeaned = y_vec - y_mean

    pacf_vec = np.zeros(total_lag_p).reshape(-1, 1)

    time_start = time.time()

    for i in range(len(pacf_vec)):

        #print(f"computing lag {i+1} of {len(pacf_vec)}")

        beta_vec_i = pacf_ar_p_fit(y_vec = y_vec,lag_p = i+1) # lag starts from 1

        pacf_vec[i] = beta_vec_i[-1]

        time_end = time.time()
        elap_time = time_end - time_start
        print(f"computed lag {i+1} of {len(pacf_vec)}, elapsed time: {round(elap_time, 2)} sec, {round(elap_time / 60, 2)} min")
        time_start = time.time()

    t1 = time.time()
    print(f"Computation finished. Total elapsed time: {round((t1-t0), 2)} sec, {round((t1-t0)/ 60, 2)} min")


    return pacf_vec


# def pacf_comp(y_vec,total_lag_p):
#
#     """
#     computes the partial autocorrelation function
#     """
#
#     time_length = len(y_vec)
#
#     y_mean = np.sum(y_vec) / time_length
#
#     y_vec_demeaned = y_vec - y_mean
#
#     pacf_vec = np.zeros(total_lag_p).reshape(-1, 1)
#
#     for i in range(len(pacf_vec)):
#         print(f"computing lag {i+1} of {len(pacf_vec)}")
#
#         beta_vec_i = pacf_ar_p_fit(y_vec = y_vec_demeaned,lag_p = i+1) # lag starts from 1
#
#         pacf_vec[i] = beta_vec_i[-1]
#
#     return pacf_vec


def adf_comp(y_vec,lag_p):

    """
    computes the augmented dickey fuller test
    """

    # creating a vector of differences
    y_vec_t = y_vec[:-1]
    y_vec_t_1 = y_vec[1:]
    y_vec_diff = y_vec_t - y_vec_t_1

    time_length = len(y_vec_diff)

    # creating OLS matrices
    Y_mat = y_vec_diff[0:time_length - lag_p]

    X_mat = np.zeros((time_length - lag_p,lag_p))
    for i in range(0,lag_p):
        i_indx = i + 1 # easier for indexing
        #print(f"{i_indx},{time_length - lag_p + i_indx}")
        selection = y_vec_diff[i_indx : time_length - lag_p + i_indx , 0]
        X_mat[:,i] = selection

    # creating vector for intercept and vector or normal (non differenced) values
    ones_vec = np.ones(time_length - lag_p).reshape(-1, 1)
    y_vec_lag = y_vec_t_1[0:time_length - lag_p]

    # creating the final X matrix
    X_mat = np.concatenate((ones_vec,y_vec_lag, X_mat), axis=1)

    # OLS regression
    beta_vec = np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T @ Y_mat

    # computing standard errors
    Y_mat_fitted = X_mat @ beta_vec
    errors_vec = Y_mat - Y_mat_fitted
    sigma_squared = (1/time_length) * errors_vec.T @ errors_vec
    covariance_matrix = sigma_squared * np.linalg.inv(X_mat.T @ X_mat)

    # computing t statistic
    gamma_param = beta_vec[1]
    gamma_var = covariance_matrix[1,1]
    gamma_SE = np.sqrt(gamma_var)

    test_statistic = gamma_param / gamma_SE

    return test_statistic

def difference_vec_comp(y_vec,seasonality):

    time_length = len(y_vec)

    y_vec_t = y_vec[:time_length - seasonality]
    y_vec_t_s = y_vec[seasonality:]

    difference_vec = y_vec_t - y_vec_t_s

    return difference_vec






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

    gamma_p = adf_comp(y_vec = relative_power_vec, lag_p = 10)


    #autocorrelation_function_vec = acf_comp(y_vec = relative_power_vec, total_lag_k = 4*24*30*12)
    # autocorrelation_function_vec = acf_comp(y_vec=relative_power_vec, total_lag_k = 4*24*1)
    #
    # time_length = len(relative_power_vec)
    #
    # fig = acf_plot(autocorrelation_function_vec,time_length)
    # plt.show()


    #pacf_vec_test = pacf_ar_p_fit(y_vec = relative_power_vec,lag_p = 4)
    # pacf_vec_test = pacf_comp(y_vec = relative_power_vec, total_lag_p = 4*24*1*1)
    #
    #
    # fig = pacf_plot(pacf_vec = pacf_vec_test,time_length = len(relative_power_vec))
    # plt.show()



    # exploring a possibility of seasonal (yearly) differences




    seasonal_diff_y_vec = difference_vec_comp(y_vec = relative_power_vec, seasonality = int(4 * 24 * 365.25))

    # autocorrelation_function_vec = acf_comp(y_vec=seasonal_diff_y_vec, total_lag_k = 4*24*30*12*9)
    #
    # time_length = len(relative_power_vec)
    #
    # fig = acf_plot(autocorrelation_function_vec,time_length)
    # plt.show()


    # pacf_vec_test = pacf_comp(y_vec = relative_power_vec, total_lag_p = 4*24*1*1)
    #
    #
    # fig = pacf_plot(pacf_vec = pacf_vec_test,time_length = len(relative_power_vec))
    # plt.show()



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





