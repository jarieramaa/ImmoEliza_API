"""
This API is used to calculate the price estimate for a house
"""

import json
from typing import Union
import pickle
import numpy as np
from flask import (
    Flask,
    abort,
    request,
)
import pandas as pd


from preprocessing import cleaning_data
from predict import prediction


app = Flask(__name__)

"""JSON_FILE is a dictionary that contains the options for each fields,
for example {'energy classes' : 'A++', 'A+' etc.}  """
_JSON_FILE = None


def _check_options(content_json: dict, field_opt: str) -> str:
    """Check if the value is in the options
    :content_json : dictionary that has got from the request
    :field_opt : str, 'property-subtype', 'kitchen-type', 'energy-class' or 'zip-code'
    :return: string, that contains the result of the check (if any errors occurs)"""
    content = content_json.get(field_opt)
    if content is None:
        return ""
    value = str(content)
    options = _JSON_FILE.get(field_opt)
    print("VALUE: ", value)
    print("field_opt: ", field_opt)
    # print("OPTIONS: ", options)
    if value is not None and value not in options:
        if len(options) > 25:
            return f"The {field_opt} field is not valid ({field_opt} '{value}'"+\
                f"does not exist).{chr(10)}"
        return (
            f"The {field_opt} field is not valid ({field_opt} '{value}' does not exist). Please, "
            + f"select one of the available options that are: {options}{chr(10)}{chr(10)}"
        )
    return ""


def _check_mandatory_fields(
    content_json: dict, living_field: str, zip_field: str, subtype_field: str
) -> str:
    """Check if the mandatory fields are in the request
    params:
        living_area : str, value that has got from the request
        zip_code : str, value that has got from the request
        property_subtype : str, value that has got from the request
    return: str, that contains error messages or None if there is no errors
    """
    living_area = content_json.get(living_field)
    zip_code = content_json.get(zip_field)
    print("zip_code: ", zip_code)
    print("type of zip_code: ", type(zip_code))
    property_subtype = content_json.get(subtype_field)
    missing_fields = ""
    if living_area is None:
        missing_fields += "'living-area' "
    if zip_code is None:
        missing_fields += "'zip-code' "
    if property_subtype is None:
        missing_fields += "'property-subtype' "
    if len(missing_fields) > 0:
        return (
            "'Living-area', 'zip-code' and 'property-subtype' "
            f"are mandatory fields. You are missing: {missing_fields}.{chr(10)}"
        )

    return ""


def _load_model() -> Union[pd.DataFrame, np.ndarray]:
    """
    Loading files that are needed in the data cleaning and prediction
    :return: dataframe and a ndarray. The dataframe has all the same colums that
    the original training model used. There is also one row with zeros. The ndarray
    is the final theta for prediction.
    """
    # save with picle to a file
    model_row = None
    theta = None
    with open("./model/model_row.pickle", "rb") as sample_row_file:
        model_row = pickle.load(sample_row_file)
    with open("./model/theta.pickle", "rb") as theta_file:
        theta = pickle.load(theta_file)
    return model_row, theta


def _check_int(content_json: dict, field_name) -> str:
    """
    this function checks if the value is an integer and returns an error message if it is not.
    :param content_json: the dictionary that has got from the request
    :param field_name: the name of the field that is being checked
    :return: str, that contains the error message or None if there is no errors
    """
    value = content_json.get(field_name)
    # print("VALUE: ", value)
    # print("value type: ", type(value))
    # print("field_name: ", field_name)
    if value is None or isinstance(value, int):
        return ""
    return (
        f"The value of the field '{field_name}' is not a integer number (uncorrect value"
        + f"is '{value}' and the type is {type(value)}). {chr(10)}"
    )


def _check_bool(content_json: dict, field_name) -> str:
    """
    this function checks if the value is a boolean and returns an error message if it is not.
    :param content_json: the dictionary that has got from the request
    :param field_name: the name of the field that is being checked
    :return: str, that contains the error message or None if there is no errors
    """
    # error_msg=
    value = content_json.get(field_name)
    if value is None or isinstance(value, bool):
        return ""
    return f"The value of the field '{field_name}' is not a boolean value (uncorrect value \
        is '{value}' and the type is {type(value)}). {chr(10)}"


def _check_unwanted(content_json: dict) -> str:
    """
    check if there are unwanted fields in the request. If there are, return an error message.
    This is done to avoid spelling mistakes in the request.
    :param content_json: the dictionary that has got from the request
    :return: str, that contains the error message or None if there is no errors
    """
    keys = content_json.keys()
    print("type of keys: ", type(keys))
    extra_keys = []
    valid_keys = [
        "property-subtype",
        "living-area",
        "kitchen-type",
        "energy-class",
        "zip-code",
        "land-area",
        "house-number",
        "swimming-pool",
        "street-address",
    ]
    for key in keys:
        if key not in valid_keys:
            extra_keys.append(key)
    if len(extra_keys) > 0:
        return "The request contains the following fields that are " +\
            f"not valid: {extra_keys}. {chr(10)}"
    return ""


@app.route("/predict", methods=["POST"])
def house_api() -> dict:
    """
    This API gets house information.
    :return: Dictionary the price estimate for the house or error message.
    """
    content_json = request.get_json()
    print("content_json: ", content_json)
    _errors = ""
    _errors = _check_mandatory_fields(
        content_json, "living-area", "zip-code", "property-subtype"
    )
    _errors += _check_options(content_json, "property-subtype")
    _errors += _check_int(content_json, "living-area")
    _errors += _check_options(content_json, "kitchen-type")
    _errors += _check_options(content_json, "energy-class")
    _errors += _check_options(content_json, "zip-code")
    _errors += _check_int(content_json, "land-area")
    _errors += _check_int(content_json, "house-number")
    _errors += _check_bool(content_json, "swimming-pool")
    _errors += _check_unwanted(content_json)

    if len(_errors) > 0:
        # abort(400, _errors)
        return {"error": _errors}

    model_row, my_theta = _load_model()
    cleaned_data = cleaning_data.preprocess(content_json, model_row)
    estimate = prediction.predict(cleaned_data, my_theta)
    return {"prediction": estimate}


@app.route("/", methods=["GET"])
def api_alive() -> dict:
    """Check if the API is alive"""
    return {"status": "alive"}


@app.route("/predict", methods=["GET"])
def return_data() -> dict:
    """return model dictionary"""
    info_dict = ""
    with open("./model/data.json", "r", encoding="utf-8") as json_data_file:
        info_dict = json.load(json_data_file)
    return info_dict


if __name__ == "__main__":
    with open("./model/options.json", "r", encoding="utf-8") as json_file:
        _JSON_FILE = json.load(json_file)
    app.run(host="0.0.0.0", port=5001, debug=True)
    # app.run(host = "0.0.0.0", port = 5000)
