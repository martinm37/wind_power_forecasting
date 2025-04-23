
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt


def original_fitted_comparison_plot(original_vec, fitted_vec):

    """
    used to make comparison plot of the original time series vector, and the one
    which was made by fitting the values from a model
    """

    fig, ax = plt.subplots()

    fig.suptitle(f"original vs fitted vectors")

    axis_vec = np.arange(0,len(original_vec))
    zeros_vec = np.zeros(len(original_vec))

    ax.plot(axis_vec, original_vec)
    ax.plot(axis_vec, fitted_vec)
    ax.plot(axis_vec, zeros_vec, "k--")

    # ax.set_ylabel("partial autocorrelation at lag k")
    # ax.set_xlabel("lag k")

    return fig


def error_plot(error_vec):

    """
    plots the errors from a model (AR) fit
    """

    fig, ax = plt.subplots()

    fig.suptitle(f"errors of the model")

    axis_vec = np.arange(0,len(error_vec))
    zeros_vec = np.zeros(len(error_vec))

    ax.plot(axis_vec, error_vec)
    ax.plot(axis_vec, zeros_vec, "k--")

    # ax.set_ylabel("partial autocorrelation at lag k")
    # ax.set_xlabel("lag k")

    return fig

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


def forecast_evaluation_plot(forecast_vec,realised_vec,initial_vec,lag_p):

    fig, ax = plt.subplots()

    fig.suptitle(f"Forecasted vs realized values")

    full_axis_vec = np.arange(0, len(initial_vec))
    init_range = full_axis_vec[:-96]
    forecast_range = full_axis_vec[len(initial_vec)-96:]

    zeros_vec = np.zeros(len(initial_vec))

    ax.plot(full_axis_vec, zeros_vec, "k--")
    ax.plot(init_range, initial_vec[:-96], "k")
    ax.plot(forecast_range, forecast_vec, label = "forecast")
    ax.plot(forecast_range, realised_vec, label = "realization")

    ax.legend()

    return fig


def forecast_comparison_plot(forecast_vec_1,forecast_vec_2,realised_vec,initial_vec,lag_p):

    fig, ax = plt.subplots()

    fig.suptitle(f"Forecasted vs realized values")

    len_1 = 2 * 96

    full_axis_vec = np.arange(0, len_1)
    init_range = full_axis_vec[:-96]
    forecast_range = full_axis_vec[len_1-96:]

    zeros_vec = np.zeros(len_1)

    ax.plot(full_axis_vec, zeros_vec, "k--")
    ax.plot(init_range, initial_vec[:96], "k")
    ax.plot(forecast_range, forecast_vec_1, label = "my forecast")
    ax.plot(forecast_range, forecast_vec_2, label="statsmodels forecast")
    ax.plot(forecast_range, realised_vec, label = "realization")

    ax.legend()

    return fig

# def forecast_evaluation_plot(forecast_vec,realised_vec):
#
#     fig, ax = plt.subplots()
#
#     fig.suptitle(f"Forecasted vs realized values")
#
#     axis_vec = np.arange(0, len(forecast_vec))
#     zeros_vec = np.zeros(len(forecast_vec))
#
#     ax.plot(axis_vec, forecast_vec, label = "forecast")
#     ax.plot(axis_vec, realised_vec, label = "realization")
#     ax.plot(axis_vec, zeros_vec, "k--")
#     ax.legend()
#
#     return fig
