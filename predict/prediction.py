"""
This module is making price prediction for houses. The prediction
is based on features like: Property sub-type, Living area, Surface
of the plot, Post code, Kitchen type, Swimming pool and Energy class.
They are given as a np.ndarray that is clened with cleaning_data.py module.
"""

import numpy as np


def _stack_ones(x_test: np.ndarray) -> np.ndarray:
    """
    Adding ones to the input data
    :X_test : ndarray
    :return: ndarray
    """
    ones = np.ones((x_test.shape[0], 1))
    x_test = np.hstack((x_test, ones))
    return x_test


def predict(x_test: np.ndarray, theta: np.ndarray) -> int:
    """
    This function is used to predict house price.
    :x_test :input data
    :theta :theta for prediction
    :return: the predicted price
    """
    x_test = x_test.to_numpy()
    x_test = _stack_ones(x_test)
    predictions = x_test.dot(theta)
    price_prediction = int(predictions[0][0])
    return round(price_prediction, -3)
