"""
The idea in this module is simple:

    1. Loading (from file) one row of data that is used to predict the
       price of the house. However, all the values are zeros. This is done
       because then we can be sure that our dataframe is exactly the same.

    2. Getting dictionary from API (or in testing phase loading it from file)

    3. Converting all columns one by one according the dictionary.

    4. Normalizing values. This is done by loading the scaler that was used
       when training the model (instance was saved to a file and now it is loaded).

"""


import pickle
import numpy as np
import pandas as pd



def _load_house() -> dict:
    """
    Just for testing. Loading a dictionary that was created by API
    :return: Dictionary with house information.
    """
    with open("./house_information.pickle", "rb") as house_information_file:
        house_information = pickle.load(house_information_file)
    return house_information


def _set_swimming_pool(house_information, model_row) -> pd.DataFrame:
    """
    set column swimming pool to one if there is a swimming pool in the house
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe where the value was added
    """
    if house_information.get("swimming-pool"):
        model_row["Swimming pool"] = 1
        return model_row
    return model_row


def _set_living_area(house_information, model_row) -> pd.DataFrame:
    """
    set 'living area' for the model row. Also some prescaling
    for the value is done as well. The original model didn't work
    otherwise.
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe where the value was added
    """
    original_value = house_information.get("living-area")
    if original_value is None:
        return model_row
    floor, ceiling = 0, 1
    _min, _max = 15, 800
    model_row["Living area"] = (original_value - _min) / (_max - _min) * (
        ceiling - floor
    ) + floor
    return model_row


def _set_land_area(house_information, model_row) -> pd.DataFrame:
    """
    set 'land area' for the model row. Also some prescaling
    for the value is done as well. The original model didn't work
    otherwise.
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe where the value was added
    """
    original_value = house_information.get("land-area")
    if original_value is None:
        return model_row
    floor, ceiling = 0, 1
    _min, _max = 15, 800
    model_row["Surface of the plot"] = (original_value - _min) / (_max - _min) * (
        ceiling - floor
    ) + floor
    return model_row


def _set_kitchen_type(house_information, model_row) -> pd.DataFrame:
    """
    convert string to numeric value
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe where the value was added
    """
    value = house_information.get("kitchen-type")
    converted_value = 0
    if value in ("Hyper equipped", "USA hyper equipped"):
        converted_value = 3
    elif value in ("Semi equipped", "USA semi equipped"):
        converted_value = 2
    elif value in ("Installed", "USA installed"):
        converted_value = 1
    elif value in ("Not installed", "USA uninstalled"):
        converted_value = 0
    model_row["Kitchen type"] = converted_value
    return model_row


def _set_energy_class(house_information, model_row) -> pd.DataFrame:
    """converting energy class to numeric value
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe where the value was added
    """
    value = house_information.get("energy-class")
    converted_value = 0
    energy_options = {
        "G_F": 0,
        "G_D": 0.5,
        "G_C": 1,
        "G": 1.5,
        "F_D": 2,
        "F_B": 2.5,
        "F": 3,
        "E_B": 3.5,
        "E": 4,
        "D_C": 4.5,
        "D": 5,
        "C_B": 5.5,
        "C": 6,
        "B": 6.5,
        "A": 7,
        "A+": 7.5,
        "A++": 8,
        "Not specified": 0,
    }
    if value in energy_options.keys():
        converted_value = energy_options.get(value)
    model_row["Energy class"] = converted_value
    return model_row


def _set_property_subtype(house_information, model_row) -> pd.DataFrame:
    """
    set property subtype for the model row
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe with added property subtype
    """
    columns_list = model_row.columns.values.tolist()
    value = house_information.get("property-subtype")
    if value in columns_list:
        model_row[value] = 1
    return model_row


def _set_post_code(house_information, model_row) -> pd.DataFrame:
    """
    set 'post code' for the model row
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe with added 'post code'
    """
    columns_list = model_row.columns.values.tolist()
    value = str(house_information.get("zip-code"))
    if value in columns_list:
        model_row[value] = 1
    return model_row


def preprocess(house_information: dict, model_row :pd.DataFrame) -> np.ndarray:
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
    model_row = _set_swimming_pool(house_information, model_row)
    model_row = _set_living_area(house_information, model_row)
    model_row = _set_land_area(house_information, model_row)
    model_row = _set_kitchen_type(house_information, model_row)
    model_row = _set_energy_class(house_information, model_row)
    model_row = _set_property_subtype(house_information, model_row)
    model_row = _set_post_code(house_information, model_row)

    return model_row


