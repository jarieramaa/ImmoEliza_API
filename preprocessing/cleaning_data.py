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
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

def save_house(house_information: dict):
    """
    Just for testing. Saving a dictionary that was created by API
    :param house_information: Dictionary with house information.
    """
    with open('./house_information.pickle', 'wb') as house_information_file:
        pickle.dump(house_information, house_information_file)


def load_house() -> dict:
    """
    Just for testing. Loading a dictionary that was created by API
    :return: Dictionary with house information.
    """
    with open('./house_information.pickle', 'rb') as house_information_file:
        house_information = pickle.load(house_information_file)
    return house_information
   

def load_scaler() -> StandardScaler:
    """
    This is the same scaler that was used when training the model.
    :return: scaler
    """
    with open('./my_scaler.pkl', 'rb') as my_standard_scaler_file:
        my_scaler = pickle.load(my_standard_scaler_file)
    return my_scaler


def load_model_row() -> pd.DataFrame:
    """
    Loading dataframe with one empty row
    :return: Dataframe with one empty row
    """
    #save with picle to a file
    with open("./model_row.pickle", "rb") as sample_row_file:
        model_row = pickle.load(sample_row_file)
        return model_row

def set_swimming_pool(house_information, model_row) ->pd.DataFrame:
    """
    set column swimming pool to one if there is a swimming pool in the house
    """
    if house_information.get("Swimming pool"):
        model_row["Swimming pool"] = 1
        return model_row
    

def set_living_area(house_information, model_row) ->pd.DataFrame:
    """
    set 'living area' for the model row. Also some prescaling 
    for the value is done as well. The original model didn't work
    otherwise.
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe with added 'living area'
    """
    original_value = house_information.get("Living area")
    print(original_value)
    a, b = 0, 1
    x, y = 15, 800
    model_row["Living area"] = (original_value - x) / (y - x) * (b - a) + a
    return model_row


def set_land_area(house_information, model_row) -> pd.DataFrame:
    """
    set land area for the model row
    """
    model_row["Surface of the plot"] = house_information.get("Land area")
    return model_row


def set_kitchen_type(house_information, model_row) -> pd.DataFrame:
    """convert string to numeric value
    :value: a string that is converted
    :return: integer that replaces the original string"""
    value = house_information.get("Kitchen type")
    converted_value = 0
    if value == "Hyper equipped" or value == "USA hyper equipped":
        converted_value = 3
    elif value == "Semi equipped" or value == "USA semi equipped":
        converted_value = 2
    elif value == "Installed" or value == "USA installed":
        converted_value = 1
    elif value == "Not installed" or value == "USA uninstalled":
        converted_value = 0
    model_row["Kitchen type"] = converted_value
    return model_row

def set_energy_class(house_information, model_row) -> pd.DataFrame:
    """convert string to numeric value
    :value: a string that is converted
    :return: integer that replaces the original string"""
    value = house_information.get("Energy class")
    converted_value = 0
    if value == "G_F":
        converted_value = 0
    elif value == "G_D":
        converted_value = 0.5
    elif value == "G_C":
        converted_value = 1
    elif value == "G":
        converted_value = 1.5
    elif value == "F_D":
        converted_value = 2
    elif value == "F_B":
        converted_value = 2.5
    elif value == "F":
        converted_value = 3
    elif value == "E_B":
        converted_value = 3.5
    elif value == "E":
        converted_value = 4
    elif value == "D_C":
        converted_value = 4.5
    elif value == "D":
        converted_value = 5
    elif value == "C_B":
        converted_value = 5.5
    elif value == "C":
        converted_value = 6
    elif value == "B":
        converted_value = 6.5
    elif value == "A":
        converted_value = 7
    elif value == "A+":
        converted_value = 7.5
    elif value == "A++":
        converted_value = 8
    elif value == "Not specified":
        converted_value = 0
    else:
        converted_value = 0
    model_row["Energy class"] = converted_value
    return model_row

def set_property_subtype(house_information, model_row) -> pd.DataFrame:
    """
    set property subtype for the model row
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe with added property subtype
    """
    columns_list = model_row.columns.values.tolist()
    value = house_information.get("property sub-type")
    if value in columns_list:
        model_row[value] = 1
    return model_row

def set_post_code(house_information, model_row) -> pd.DataFrame:
    """
    set 'post code' for the model row
    :house_information: dictionary with house information
    :model_row: dataframe with one row
    :return: dataframe with added 'post code'
    """
    columns_list = model_row.columns.values.tolist()
    value = str(house_information.get("Post code"))
    if value in columns_list:
        model_row[value] = 1
    return model_row


def preprocess(house_information: dict, my_scaler: StandardScaler) -> np.ndarray:
    """
    Converting the house information ready for use with prediction model. 
    1. Converting non-numeric values to numeric values, 
    2. Taking care of missing values, 
    3. Converting values to dummies. 
    :param house_information: Dictionary with house information.
    :return: Dictionary with cleaned house information. Also a possible error message
    """
    model_row = load_model_row()
    model_row = set_swimming_pool(house_information, model_row)
    model_row = set_living_area(house_information, model_row)
    model_row = set_land_area(house_information, model_row)
    model_row = set_kitchen_type(house_information, model_row)
    model_row = set_energy_class(house_information, model_row)
    model_row = set_property_subtype(house_information, model_row)
    model_row = set_post_code(house_information, model_row)

    x_test = model_row.to_numpy()

    with open('./x_test_api.pkl', 'wb') as final_file:
        pickle.dump(x_test, final_file)

    return 0, ""


if __name__ == "__main__":
    house_information = load_house()
    print(house_information)
    my_scaler = load_scaler()
    preprocess(house_information, my_scaler)


