"""This module is for testing flack_challenge.py API"""

from io import BytesIO
import json
import requests
import pycurl



def test_api():
    """This is a test function for the API."""

    my_result = requests.post(
        "http://127.0.0.1:5000/house",
        params={
            "property-subtype": "CASTLE",
            "living-area": 300,
            "kitchen-type": "Hyper equipped",
            "swimming-pool": "true",
            "energy-class": "C_B",
            "street-address": "Rue Royale",
            "house-number": "190",
            "post-code": "1000",
        },
    )
    print(my_result.text)


"""    my_result = requests.post(
        "http://127.0.0.1:5000/house",
        params={
            "property-subtype": 2500,
            "living-area": 2000,
            "land-area": 1800,
            "kitchen-type": "",
            "swimming-pool": "",
            "energy-class": "",
            "street-address": "",
            "house-number": "",
            "post-code": "",
        },
    )
    print(my_result.text)"""


if __name__ == "__main__":
    test_api()
