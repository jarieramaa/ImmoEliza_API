"""This API is used to calculate the price estimate for a house


  API                   COLUMN                  MODEL
("property-subtype")    "property sub-type"    -> Dummies
("living_area")         "Living area"
("post-code")           "Post code"            -> Dummies
("kitchen-type")        "Kitchen type"          [options]
("swimming-pool")        "Swimming pool"          bool
("energy-class")        "Energy class"          [options]
("street")
("house-number")
"""

import json
import pickle
from typing import Optional

import preprocessing.cleaning_data as cleaning_data
import predict.prediction as prediction

from flask import (
    Flask,
    request,
)


app = Flask(__name__)

JSON_FILE = None


def check_options(value: str, field_opt: str) -> str:
    """Check if the value is in the options
    :value : str, value that has got from the request
    :field_opt : str, 'property_subtype', 'kitchen_type', 'energy_class' or 'post_code'
    :return: ste, that contains the result of the check"""
    options = JSON_FILE.get(field_opt)
    if value is not None and value not in options:
        if len(options) > 25:
            return f"The {field_opt} field is not valid (uncorrect value is:{value}).{chr(10)}"
        return (
            f"The {field_opt} field is not valid (uncorrect value is:{value}). Please, "
            + f"select one of the available options that are: {options}{chr(10)}{chr(10)}"
        )
    return ""


def check_mandatory_fields(
    living_area: str, post_code: str, property_subtype: str
) -> str:
    """Check if the mandatory fields are in the request
    params:
        living_area : str, value that has got from the request
        post_code : str, value that has got from the request
        property_subtype : str, value that has got from the request
    return: str, that contains error messages or None if there is no errors
    """
    missing_fields = ""
    if living_area is None:
        missing_fields += "'living area' "
    if post_code is None:
        missing_fields += "'post code' "
    if property_subtype is None:
        missing_fields += "'property subtype' "
    if len(missing_fields) > 0:
        return (
            "'Living area', 'post code' and 'property subtype' "
            + f"are mandatory fields. You are missing: {missing_fields}.{chr(10)}{chr(10)}"
        )
    return ""


def convert_to_int(value, field_name) -> tuple[int, str]:
    """
    Convert the value to int. As the value is not mandatory, it's ok that it's 'None'
    :value : str, value that has got from the request
    :field_name : str, field_name is used in the error message
    :return: int, that contains the result of the conversion and possible error message
    """
    if value is None:
        return 0, ""
    if value.isnumeric():
        return int(value), ""
    return (
        0,
        f"The value of the field '{field_name}' is not a number"
        + f" (uncorrect value is '{value}').{chr(10)}{chr(10)}",
    )


def convert_to_bool(value, field_name) -> tuple[bool, str]:
    """
    converting value to boolean
    """
    print("start, value is:", value)
    if value is None:
        return False, ""
    if value.lower() == "true":
        return True, ""
    if value.lower() == "false":
        return False, ""
    return (
        False,
        f"The value of the field '{field_name}' is not a boolean"
        + f"(uncorrect value is '{value}').{chr(10)}{chr(10)}",
    )


@app.route("/predict", methods=["POST"])
def house_api() -> dict:
    """
    This API gets house information.
    :return: Dictionary the price estimate for the house or error message.
    """
    content = request.args

    property_subtype = content.get("property-subtype")
    living_area = content.get("living-area")
    land_area = content.get("land-area")
    kitchen_type = content.get("kitchen-type")
    swimming_pool = content.get("swimming-pool")
    energy_class = content.get("energy-class")
    street = content.get("street-address")
    house = content.get("house-number")
    post_code = content.get("post-code")

    error_messages = ""
    error_messages += check_mandatory_fields(living_area, post_code, property_subtype)
    error_messages += check_options(property_subtype, "property_subtype")
    error_messages += check_options(kitchen_type, "kitchen_type")
    error_messages += check_options(energy_class, "energy_class")
    error_messages += check_options(post_code, "post_code")

    living_area, error_message = convert_to_int(living_area, "living area")
    error_messages += error_message
    land_area, error_message = convert_to_int(land_area, "land area")
    error_messages += error_message
    house, error_message = convert_to_int(house, "house")
    error_messages += error_message
    post_code, error_message = convert_to_int(post_code, "post code")
    error_messages += error_message
    swimming_pool, error_message = convert_to_bool(swimming_pool, "swimming pool")
    error_messages += error_message

    if len(error_messages) > 0:
        return {"error": error_messages}

    house_information = {
        "property sub-type": property_subtype,
        "Living area": living_area,
        "Land area": land_area,
        "Kitchen type": kitchen_type,
        "Swimming pool": swimming_pool,
        "Energy class": energy_class,
        "Street": street,
        "House": house,
        "Post code": post_code,
    }

    # error_msgs = ""
    cleaned_data, errors = cleaning_data.preprocess(house_information)
    return {"prediction": "100"}


"""    error_msgs += errors
    with open('./model/theta.pickle', 'rb') as predictions_file:
        theta = pickle.load(theta)
    prediction_result, errors = prediction.predict(theta, cleaned_data)
    error_msgs += errors
    if len(error_messages) > 0:
        return {"error": error_msgs}
    return prediction_result"""


@app.route("/", methods=["GET"])
def api_alive() -> str:
    """Check if the API is alive"""
    return {"status": "alive"}


@app.route("/predict", methods=["GET"])
def return_data() -> str:
    """Check if the API is alive"""
    info_dict = { "data": " {\"living-area\": int, \"property-subtype\": \"Optional[ \"APARTMENT_BLOCK\" \
| \"BUNGALOW\" | \"CASTLE\" | \"CHALET\" | \"COUNTRY_COTTAGE\" | \"DUPLEX\" \
| \"EXCEPTIONAL_PROPERTY\" | \"FARMHOUSE\" | \"FLAT_STUDIO\" | \"GROUND_FLOOR\" \
| \"KOT\" | \"LOFT\" | \"MANOR_HOUSE\" | \"MANSION\" | \"MIXED_USE_BUILDING\" \
| \"OTHER_PROPERTY\" | \"PENTHOUSE\" | \"SERVICE_FLAT\" | \"TOWN_HOUSE\" \
| \"TRIPLEX\" | \"VILLA\"]\", \
\"post-code\": \"int\", \
\"land-area\": \"Optional[int]\", \
\"kitchen-type\": \"Optional[ \"Hyper equipped\" | \"Installed\" \
| \"Not installed\" | \"Semi equipped\" | \"USA hyper equipped\" \
| \"USA installed\" | \"USA semi equipped\" | \"USA uninstalled\" ]\", \
    \"swimming-pool\": \"Optional[bool]\", \
    \"energy-class\": \"Optional[\"A\" | \"A+\" | \"B\" | \"C\" | \"C_B\"\ \
    | \"D\" | \"E\" | \"F\" | \"F_B\" | \"G\" | \"G_C\" | \"G_D\" ]\", \
\"street\": \"Optional(str)\", \
\"house-number\": \"Optional(int)\" "}
    return info_dict

if __name__ == "__main__":
    with open("./preprocessing/options.json", "r", encoding="utf-8") as json_file:
        JSON_FILE = json.load(json_file)
    app.run(debug=True) # app.run(port=5000)


    
