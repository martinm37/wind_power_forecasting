
"""
holds class for an AR(p) model, with model fitting and forecasting methods
"""

import numpy as np

from src.utils.utils import StatisticalModelSolution


class AutoRegressiveModel:

    def __init__(self,lag_order_p):

        self.lag_order_p = lag_order_p
        self.model_fit_solution = None # holds the results of the model_fitting method


    def model_fitting(self,data_vector):

        """
        computes the AR(p) model

        original vector y_vec has dimensions of T x 1
        new vectors will have dimensions (T - lag_p) x 1
        """

        time_length = len(data_vector)
        data_vec_cut = data_vector[0:time_length - self.lag_order_p]
        X_mat = np.zeros((time_length - self.lag_order_p, self.lag_order_p))

        for i in range(0, self.lag_order_p):
            i_indx = i + 1  # easier for indexing
            # print(f"{i_indx},{time_length - lag_p + i_indx}")
            selection = data_vector[i_indx: time_length - self.lag_order_p + i_indx, 0]
            X_mat[:, i] = selection

        # vector for the intercept terms
        ones_vec = np.ones(time_length - self.lag_order_p).reshape(-1, 1)
        X_mat = np.concatenate((ones_vec, X_mat), axis=1)

        # OLS estimation
        beta_vec = np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T @ data_vec_cut

        # errors computation
        Y_mat_fitted = X_mat @ beta_vec
        errors_vec = data_vec_cut - Y_mat_fitted

        # exporting
        model_solution = StatisticalModelSolution(beta_vector=beta_vec,
                                                  Y_mat=data_vec_cut,
                                                  Y_mat_fitted=Y_mat_fitted,
                                                  errors_vector=errors_vec)

        self.model_fit_solution = model_solution

        return model_solution


    def model_forecasting(self, initialization_vector, forecast_horizon):

        """
        initialization_vector - newest observations on top
        initialization_vector is one element shorter than self.beta_vec,
        to account for the intercept term
        """

        forecast_vec = np.zeros(forecast_horizon)

        for h in range(forecast_horizon):
            one_array = np.array([[1]])
            y_vec = np.concatenate((one_array,initialization_vector),axis = 0)
            forecast_h = y_vec.T @ self.model_fit_solution.beta_vector
            forecast_vec[h] = y_vec.T @ self.model_fit_solution.beta_vector
            # now overwrite the starting_y_vec
            kept_part = initialization_vector[:-1]
            initialization_vector = np.concatenate((forecast_h,kept_part),axis = 0)


        return forecast_vec







