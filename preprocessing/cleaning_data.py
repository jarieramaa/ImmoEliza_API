"""
This module:

    1. Loads (from file) one row of data that is used to predict the
       price of the house. However, all the values are zeros. This is done
       because then we can be sure that our dataframe is exactly the same.

    2. Getting dictionary from API

    3. Converting all columns one by one according the properties_meta.json -file (house_meta).
"""


import numpy as np
import pandas as pd


def _print_df(dataf: pd.DataFrame):
    """
    Made for testing. Printing the dataframe's columns that has
    some values (there is over 200 columns in the model_row)
    :dataf: dataframe to print
    """
    columns = dataf.columns.values.tolist()
    selected_columns = []
    for column in columns:
        if dataf[column].sum() > 0:
            selected_columns.append(column)
    print(dataf[selected_columns])


def _one_hot_encoding(
    content_json: dict, feature_name: str, model_row: pd.DataFrame
) -> pd.DataFrame:
    """
    set one-hot encoding for the model row
    :content_json: json with the content read from the API
    :feature_name: name of the feature
    :model_row: dataframe with one row. This will be modified
    :return: dataframe (model_row) with added one-hot encoding
    """
    columns_list = model_row.columns.values.tolist()
    # column_name = f_meta.get(feature_name).get("df_name")
    column_name = str(content_json.get(feature_name))
    if column_name in columns_list:
        model_row[column_name] = 1
    return model_row


def _set_boolean(
    content_json: dict, feature_name: str, model_row: pd.DataFrame, f_meta: dict
) -> pd.DataFrame:
    """
    set column swimming pool to one if there is a swimming pool in the house
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe where the value was added
    """
    value = content_json.get(feature_name)
    if value:
        column_name = f_meta.get(feature_name).get("df_name")
        model_row[column_name] = 1
    return model_row


def _convert_values(content_json, feature_name, model_row, f_meta) -> pd.DataFrame:
    """converting energy class to numeric value
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe where the value was added
    """
    value = content_json.get(feature_name)
    data_cleaning = f_meta.get(feature_name).get("data_cleaning")
    if data_cleaning is not None:
        mean_value = data_cleaning.get("mean_value")
        conversion_table = data_cleaning.get("conversion_table")
        df_name = f_meta.get(feature_name).get("df_name")
        # if value = None, then use mean_value, otherwise use conversion_table
        new_value = mean_value
        conv_value = conversion_table.get(value)
        if conv_value is not None:
            new_value = conv_value
        model_row[df_name] = new_value
    return model_row


def _normalise_values(
    content_json: dict, feature_name: str, model_row: pd.DataFrame, f_meta: dict
) -> pd.DataFrame:
    """ """
    value = content_json.get(feature_name)
    df_name = f_meta.get(feature_name).get("df_name")
    data_cleaning = f_meta.get(feature_name).get("data_cleaning")
    if data_cleaning is not None and df_name is not None and value is not None:
        min_value = data_cleaning.get("min")
        max_value = data_cleaning.get("max")
        floor, ceiling = 0, 1
        model_row[df_name] = (value - min_value) / (max_value - min_value) * (
            ceiling - floor
        ) + floor
    return model_row


def preprocess(content_json: dict, model_row: pd.DataFrame, f_meta) -> np.ndarray:
    """
    Converting the house information ready for use with prediction model.
    1. Converting non-numeric values to numeric values,
    2. Taking care of missing values,
    3. Converting values to dummies.
    param :
    :house_information: Dictionary with house information.
    :std_scaler: Standard scaler that was used to train the model.
    :model_row: Dataframe with one row, this contains all required columns and onw row with zeros.
    :return: Dictionary with cleaned house information. Also a possible error message
    """
    # content_json_keys = content_json.keys()
    f_meta_keys = f_meta.keys()
    for feature_name in f_meta_keys:
        data_cleaning = f_meta.get(feature_name).get("data_cleaning")
        if data_cleaning is None:
            continue
        cleaning_method = data_cleaning.get("method")
        if cleaning_method == "one-hot" and feature_name in content_json:
            _one_hot_encoding(content_json, feature_name, model_row)
        elif cleaning_method == "normalise" and feature_name in content_json:
            _normalise_values(content_json, feature_name, model_row, f_meta)
        elif cleaning_method == "bool" and feature_name in content_json:
            _set_boolean(content_json, feature_name, model_row, f_meta)
        elif cleaning_method == "convert":  # mean for empty values
            _convert_values(content_json, feature_name, model_row, f_meta)
    return model_row
