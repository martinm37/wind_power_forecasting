"""
forecasting with the AR(p) model
"""

import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.wind_power_forecasting.data_visualization.plotting_functions import (
    forecast_plot_three_models,
)
from src.wind_power_forecasting.mysql_query_functions.mysql_query_functions import (
    SQLFunctionsWrapper,
)
from src.wind_power_forecasting.utils.paths import (
    get_figures_path,
    get_model_files_path,
)
from src.wind_power_forecasting.utils.utils import adjusted_current_time
from wind_power_forecasting.data_structures.database_connectors import (
    MySQLConnectionData,
)


def ar_p_model_forecasting(sql_functions_wrapper: SQLFunctionsWrapper, lag_p: int):

    # selecting past observations to initialize forecasting
    # -----------------------------------------------------
    # TODO:
    # 2) somehow make it robust to NULL values, with linear interpolation/extrapolation or smth

    # current_time = datetime.datetime(2025,4,19,13,00)
    current_time = adjusted_current_time()[1]

    select_query = """
                    SELECT datetime,rescaled_power
                    FROM wind_power_transformed_tbl
                    WHERE datetime <= %s
                    ORDER BY datetime DESC
                    LIMIT 96;
                    """

    query_data = (current_time,)
    # if there is just a single param, it has to be like (.,) !!!!

    select_query_outputs = sql_functions_wrapper.select_query_wrapper(
        query_text=select_query, query_data=query_data
    )
    cursor_object = select_query_outputs.cursor

    data = cursor_object.fetchall()
    col_names = cursor_object.column_names
    data_df = pd.DataFrame(data=data, columns=col_names)

    last_day_vec = data_df["rescaled_power"].to_numpy().reshape(-1, 1)
    forecast_init_vec = last_day_vec[:lag_p]

    # loading pickle file of the trained/fitted model
    # ----------------------------------------------
    with open(
        os.path.join(get_model_files_path(), f"ar_p{lag_p}_model_pickle.pkl"), mode="rb"
    ) as pkl_file:
        ar_p_model = pickle.load(pkl_file)

    # 'rb' model means "Open the file for reading in binary format.
    # Raises an I/O error if the file does not exist."

    # forecasting
    # ------------------
    forecast_vec = ar_p_model.model_forecasting(
        initialization_vector=forecast_init_vec, forecast_horizon=96
    )

    return forecast_vec, last_day_vec


if __name__ == "__main__":
    connection_data = MySQLConnectionData(
        user=os.environ["STANDARD_USER_1"],
        password=os.environ["STANDARD_USER_1_PASSWORD"],
        host="localhost",
        port=3306,
        database="wind_power_db",
        datatable="wind_power_transformed_tbl",
    )

    sql_functions_wrapper = SQLFunctionsWrapper(connection_data)

    # for a single model:
    # -------------------
    # lag_p = 15
    # forecast_vec_p_15,last_day_vec = ar_p_model_forecasting(sql_functions_wrapper,lag_p=lag_p)
    # current_time = adjusted_current_time()[1]
    #
    # # plotting
    # fig = forecast_plot(forecast_vec_p_15,initial_vec=np.flip(last_day_vec.flatten()))
    # #plt.show()
    # plt.savefig(os.path.join(get_figures_path(),
    # f"ar_p_{lag_p}_forecast_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}.svg"))

    # comparison of three models:
    # ---------------------------
    forecast_vec_15, last_day_vec = ar_p_model_forecasting(
        sql_functions_wrapper, lag_p=15
    )
    forecast_vec_48 = ar_p_model_forecasting(sql_functions_wrapper, lag_p=48)[0]
    forecast_vec_96 = ar_p_model_forecasting(sql_functions_wrapper, lag_p=96)[0]

    current_time = adjusted_current_time()[1]

    fig = forecast_plot_three_models(
        forecast_vec_15,
        forecast_vec_48,
        forecast_vec_96,
        initial_vec=np.flip(last_day_vec.flatten()),
    )
    # plt.show()
    plt.savefig(
        os.path.join(
            get_figures_path(),
            f"three_ar_p_forecasts_{current_time.year}_{current_time.month}_{current_time.day}_{current_time.hour}_{current_time.minute}.svg",
        )
    )
