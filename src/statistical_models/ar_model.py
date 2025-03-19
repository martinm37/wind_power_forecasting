


import numpy as np


from src.utils.utils import StatisticalModelSolution


def ar_p_model_comp(y_vec,lag_p):

    """
    computes the AR(p) model

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

    # vector for the intercept terms
    ones_vec = np.ones(time_length - lag_p).reshape(-1,1)
    X_mat = np.concatenate((ones_vec,X_mat),axis=1)

    # OLS estimation
    beta_vec = np.linalg.inv(X_mat.T @ X_mat) @ X_mat.T @ Y_mat

    # errors computation
    Y_mat_fitted = X_mat @ beta_vec
    errors_vec = Y_mat - Y_mat_fitted

    model_solution = StatisticalModelSolution(beta_vector = beta_vec,
                                              Y_mat = Y_mat,
                                              Y_mat_fitted = Y_mat_fitted,
                                              errors_vector=errors_vec)

    return model_solution





