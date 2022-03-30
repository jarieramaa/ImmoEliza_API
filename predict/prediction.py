"""
This module is making price prediction for houses. As a input
the model needs the following data: property sub-type, Living area,
Post code, Kitchen type, Swimming pool and Energy class. They are
given as a np.ndarray that is clened with cleaning_data.py module.
"""

import pickle
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def _load_theta() -> np.ndarray:
    """
    load the theta that is used to calculate the predictions
    """
    with open(
        "/Users/jari/DATA/Projects/ImmoEliza_API/model/theta.pickle", "rb"
    ) as theta_file:
        theta = pickle.load(theta_file)
        return theta


def _load_x_test_data() -> pd.DataFrame:
    """
    read test data from csv file. This is used only for testing
    :return: DataFrame that contains the test data
    """
    with open(
        "/Users/jari/DATA/Projects/ImmoEliza_API/predict/X_test_sample.pickle", "rb"
    ) as x_test_file:
        x_test = pickle.load(x_test_file)
        print("LOAD - X_test.shape", x_test.shape)
        print("LOAD - type(X_test)", type(x_test))
        print("X_TEST FILEc: ", x_test)
        return x_test


def _load_y_test_data() -> pd.DataFrame:
    """
    Read some test data from csv file. This is not used only for testing
    :return: DataFrame that contains the test data
    """
    with open(
        "/Users/jari/DATA/Projects/ImmoEliza_API/predict/y_test_sample.pickle", "rb"
    ) as y_test_file:
        y_test = pickle.load(y_test_file)
        print("LOAD - y_test.shape", y_test.shape)
        print("LOAD - type(y_test)", type(y_test))
        return y_test


def _model(x_test: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """
    This function is used to calculate the predictions of the model
    param:
        X: input data
        theta: linear regression parameters
    """
    return x_test.dot(theta)


def _stack_ones(x_test: np.ndarray) -> np.ndarray:
    """adding ones to the input data
    :X_test: input data
    """
    ones = np.ones((x_test.shape[0], 1))
    x_test = np.hstack((x_test, ones))
    return x_test


def _show_scatter(y_test, predictions):
    """
    This function is used to show the scatter plot of the predictions.
    Only needed during testing
    :y_test: actual values
    :predictions: predicted values
    """
    print("PREDICT - y_test.shape", y_test.shape)
    print("PREDICT - predictions.shape", predictions.shape)
    plt.figure(figsize=(12, 10))
    plt.scatter(y_test, predictions)
    plt.show()


def _coef_determination(y_test, pred):
    """
    Calculate how good the model actually is.
    :y: actual values
    :pred: predicted values
    """
    u_value = ((y_test - pred) ** 2).sum()
    v_value = ((y_test - y_test.mean()) ** 2).sum()
    return 1 - u_value / v_value


def predict(x_test: np.ndarray, theta: np.ndarray) -> int:
    """
    This function is used to predict house price.
    :X_test :
    """
    x_test = x_test.to_numpy()
    #x_test = std_scaler.transform(x_test)
    x_test = _stack_ones(x_test)
    predictions = _model(x_test, theta)
    value = predictions[0][0]
    print("#"*100)
    print("ESTIMATE:",value , "eur")
    return value


def test_predictions():
    """
    This function is used to test the predictions
    """
    X_test = _load_x_test_data()
    print("X_test.shape", X_test.shape)
    y_test = _load_y_test_data()
    theta = _load_theta()
    std_scaler = _load_scaler()
    #X_test = std_scaler.transform(X_test)
    X_test = _stack_ones(X_test)
    predictions = _model(X_test, theta)
    _show_scatter(y_test, predictions)
    print("#"*100)
    print(predictions)
    #predict(X_test)


if __name__ == "__main__":
    test_predictions()
