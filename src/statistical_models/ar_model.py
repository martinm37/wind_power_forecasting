


import numpy as np


from src.utils.utils import StatisticalModelSolution


def ar_p_model_comp(y_vec,lag_p):

    """
    computes the AR(p) model

    original vector y_vec has dimensions of T x 1
    new vectors will have dimensions (T - lag_p) x 1
    """

    time_length = len(y_vec)
    y_vec_cut = y_vec[0:time_length - lag_p]
    X_mat = np.zeros((time_length - lag_p,lag_p))

    for i in range(0,lag_p):
        i_indx = i + 1 # easier for indexing
        #print(f"{i_indx},{time_length - lag_p + i_indx}")
        selection = y_vec[i_indx : time_length - lag_p + i_indx , 0]
        X_mat[:,i] = selection

    # vector for the intercept terms
    ones_vec = np.ones(time_length - lag_p).reshape(-1,1)
    X_mat = np.concatenate((ones_vec,X_mat),axis=1)

    # OLS estimation
    beta_vec = np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T @ y_vec_cut

    # errors computation
    Y_mat_fitted = X_mat @ beta_vec
    errors_vec = y_vec_cut - Y_mat_fitted

    model_solution = StatisticalModelSolution(beta_vector = beta_vec,
                                              Y_mat = y_vec_cut,
                                              Y_mat_fitted = Y_mat_fitted,
                                              errors_vector=errors_vec)

    return model_solution


def ar_p_model_forecast_comp(starting_y_vec, beta_vec, horizon):

    """
    starting_y_vec is one element shorter than beta_vec,
    to account for the intercept term
    """

    forecast_vec = np.zeros(horizon)

    for h in range(horizon):
        one_array = np.array([[1]])
        y_vec = np.concatenate((one_array,starting_y_vec),axis = 0)
        forecast_h = y_vec.T @ beta_vec
        forecast_vec[h] = y_vec.T @ beta_vec
        # now overwrite the starting_y_vec
        kept_part = starting_y_vec[:-1]
        starting_y_vec = np.concatenate((forecast_h,kept_part),axis = 0)



    return forecast_vec







