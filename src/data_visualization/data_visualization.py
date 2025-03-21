
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import datetime


from src.utils.paths import get_data_path, get_data_file


def wind_series_plotter(time_vec,power_vec,frequency):

    fig, ax = plt.subplots()

    fig.suptitle(f"Wind power time series, {frequency} frequency")

    ax.plot(time_vec,power_vec)
    ax.set_ylabel("power [MW]")
    ax.set_xlabel("time")

    return fig

def wind_series_plotter_rescaled(time_vec,power_vec,frequency):

    fig, ax = plt.subplots()

    fig.suptitle(f"Wind power time series, rescaled, {frequency} frequency")

    ax.plot(time_vec,power_vec)
    ax.set_ylabel("power [% of total capacity]")
    ax.set_xlabel("time")

    return fig


def wind_series_plotter_with_capacity(time_vec,power_vec,cap_vec,frequency):

    fig, ax = plt.subplots()

    fig.suptitle(f"Wind power time series, {frequency} frequency")

    ax.plot(time_vec,power_vec, label="wind power")
    ax.plot(time_vec, cap_vec, label="total capacity")
    ax.set_ylabel("power [MW]")
    ax.set_xlabel("time")
    ax.legend()

    return fig




