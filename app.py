"""
This API is used to calculate the price estimate for a house
"""
import os
import json
from typing import Union
import pickle
import numpy as np
from flask import (
    Flask,
    request,
)
import pandas as pd

from preprocessing import cleaning_data
from predict import prediction
from model import validate_json


app = Flask(__name__)


class MetaData:
    """
    This class is used to store the meta data for each feature.
    """

    def __init__(self):
        self.meta_data = None
        self.refresh()

    def refresh(self):
        """
        This function loads meta_data from correct folder. Folder is
        defined in the setup_option.json file.
        """
        with open("./model/setup_options.json", "r", encoding="utf-8") as json_file:
            setup_options = json.load(json_file)
        subfolder = setup_options.get("active")
        with open(
            f"./model/{subfolder}/features_meta_data.json", "r", encoding="utf-8"
        ) as json_file:
            self.meta_data = json.load(json_file)

    @property
    def get_meta(self):
        """Getter that returns the meta data"""
        return self.meta_data


# A MetaData object to store feature_meta_data.json file
_F_META = MetaData()


def _check_options(content_json: dict, field_opt: str) -> str:
    """Check if the value is in the options
    :content_json : dictionary that has got from the request
    :field_opt : str, 'property-subtype', 'kitchen-type', 'energy-class' or 'zip-code'
    :return: string, that contains the result of the check (if any errors occurs)"""
    content = content_json.get(field_opt)
    if content is None:
        return ""
    value = str(content)
    options = _F_META.get_meta.get(field_opt).get("options")
    if value is not None and value not in options:
        if len(options) > 25:
            return (
                f"The {field_opt} field is not valid ({field_opt} '{value}'"
                + f"does not exist).{chr(10)}"
            )
        return (
            f"The {field_opt} field is not valid ({field_opt} '{value}' does not exist). Please, "
            + f"select one of the available options that are: {options}{chr(10)}{chr(10)}"
        )
    return ""


def _check_mandatory_fields(content_json: dict) -> str:
    """Check if the mandatory fields are in the request
    :param content_json: the dictionary that has got from the request
    return: str, that contains error messages or empty string if there is no errors
    """
    # list of mandatory_properties (for ex. 'area', 'zip-code' and 'property-subtype')
    mandatory_properties = []
    for prop in _F_META.get_meta.keys():
        if _F_META.get_meta.get(prop).get("mandatory"):
            mandatory_properties.append(prop)

    missing_fields = ""
    for name in mandatory_properties:
        value = content_json.get(name)
        if value is None:
            missing_fields += f"'{name}' "

    if len(missing_fields) > 0:
        return (
            "'area', 'zip-code' and 'property-subtype' "
            f"are mandatory fields. You are missing: {missing_fields}.{chr(10)}{chr(10)}"
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
    with open("./model/setup_options.json", "r", encoding="utf-8") as json_file:
        setup_options = json.load(json_file)
    subfolder = setup_options.get("active")
    with open(f"./model/{subfolder}/model_row.pickle", "rb") as sample_row_file:
        model_row = pickle.load(sample_row_file)
    with open(f"./model/{subfolder}/theta.pickle", "rb") as theta_file:
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
    if value is None or isinstance(value, int):
        return ""
    return (
        f"The value of the field '{field_name}' is not a integer number (uncorrect value"
        + f"is '{value}' and the type is {type(value)}). {chr(10)}{chr(10)}"
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
    return (
        f"The value of the field '{field_name}' is not a boolean value (the type"
        f"is {type(value)} and the uncorrect value is '{value}'. {chr(10)}{chr(10)}"
    )


def _check_types(content_json: dict) -> str:
    """
    This function checks if the values are correct types and returns
    an error message if it is not.
    :param content_json: the dictionary that has got from the request
    :return: str, that contains the error message(s) if there is no errors. If
    there is no errors, it returns an empty string.
    """
    content_json_keys = content_json.keys()
    _errors = ""
    for property_name in content_json_keys:
        type_of_data = _F_META.get_meta.get(property_name).get("type")
        if type_of_data == "int":
            _errors += _check_int(content_json, property_name)
        elif type_of_data == "bool":
            _errors += _check_bool(content_json, property_name)
        elif type_of_data == "options":
            _errors += _check_options(content_json, property_name)
        elif type_of_data == "str":
            pass
        else:
            _errors += f"Error in features_meta_data.json file . The type of the \
                field '{property_name}' is not valid (uncorrect \
                    value is '{type_of_data}'. {chr(10)}{chr(10)}"
    return _errors


def _check_unwanted(content_json: dict) -> str:
    """
    check if there are unwanted fields in the request. If there are, return an error message.
    This is done to avoid spelling mistakes in the request.
    :param content_json: the dictionary that has got from the request
    :return: str, that contains the error message or None if there is no errors
    """
    allowed_keys = _F_META.get_meta.keys()
    request_keys = content_json.keys()
    unwanted_keys = []
    for key in request_keys:
        if key not in allowed_keys:
            unwanted_keys.append(key)

    if len(unwanted_keys) > 0:
        return (
            "The request contains the following fields that are "
            f"not valid: {unwanted_keys}. {chr(10)}{chr(10)}"
        )
    return ""


@app.route("/predict", methods=["POST"])
def house_api() -> dict:
    """
    This API gets house information.
    :return: Dictionary the price estimate for the house or error message.
    """
    content_json = request.get_json()
    _errors = ""
    _errors += _check_unwanted(content_json)
    if not _errors:
        _errors = _check_mandatory_fields(content_json)
        _errors += _check_types(content_json)
    if len(_errors) > 0:
        return {"error": _errors}
    model_row, my_theta = _load_model()
    cleaned_data = cleaning_data.preprocess(content_json, model_row, _F_META.get_meta)
    estimate = prediction.predict(cleaned_data, my_theta)
    return {"prediction": estimate}


@app.route("/", methods=["GET"])
def api_alive() -> dict:
    """
    Check if the API is alive
    :return: Dictionary with the status of the API
    """
    return {"status": "alive"}


@app.route("/setup", methods=["GET"])
def setup_info() -> dict:
    """
    Gives instructions and shows what is currently selected model. Selected model is
    just a foder name that contains three files: model_row.pickle, theta.pickle and
    features_meta_data.json. The last one defines the API interface, data types and also how
    cleaning should be done.
    {data: {"active": "MAX",
     "available_options: ["CHALLENGE", "OPTIMAL", "MAX"]}}
    :return: Dictionary with the info what model is active and what are available options"""
    with open("./model/setup_options.json", "r", encoding="utf-8") as json_file:
        setup_options = json.load(json_file)
    return setup_options


@app.route("/setup", methods=["POST"])
def setup() -> dict:
    """
    Changes current model.
    {"activate": "MAX",}
    :return: Dictionary with the status of the API for ex. {'status': 'MAX activated'}
    """
    with open("./model/setup_options.json", "r", encoding="utf-8") as json_file:
        setup_options = json.load(json_file)
    available_options = setup_options.get("available_options")
    content_json = request.get_json()
    activate = content_json.get("activate")
    if activate is None:
        return {
            "error": (
                "Please, make sure your json is correct. The format is"
                '{"activate" : <selection>}. <selection> should be one of the following: '
            )
            + str(available_options)
        }
    if activate not in available_options:
        return {
            "error": (
                f"{activate} is not available."
                f"Please choose one of the following available options: {available_options}"
            )
        }
    setup_options["active"] = activate
    with open("./model/setup_options.json", "w", encoding="utf-8") as json_file:
        json.dump(setup_options, json_file)
    _F_META.refresh()
    return {"status": f"'{activate}' is now activated"}


@app.route("/predict", methods=["GET"])
def return_data() -> dict:
    """
    return model dictionary
    :return: Dictionary with the model
    """
    data_info = validate_json.generate_info(_F_META.get_meta)
    return {"data": data_info}


if __name__ == "__main__":
    _F_META.refresh()
    port = os.environ.get("PORT", 5000)
    #app.run(host="0.0.0.0", port=port, debug=True)
    app.run(host="0.0.0.0", port=port)
