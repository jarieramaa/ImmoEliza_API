"""This module is for testing app.py API"""


import requests
import pycurl
from io import BytesIO
import json


def test_api():
    """This is a test function for the API."""
    
    my_result = requests.post(
        "http://127.0.0.1:5000/predict",
        params={
            "property-subtype": "FARMHOUSE",
            "living-area": 300,
            "land-area": 581,
            "kitchen-type": "Not installed",
            "swimming-pool": False,
            "energy-class": "F",
            "street-address": "no_street",
            "house-number": "190",
            "post-code": "4560",
        },
    )
    print(my_result.text)

def test_alive():
    """This is a test function for the API."""
    crl = pycurl.Curl()
    buffer = BytesIO()
    # buffer = StringIO()
    crl.setopt(crl.URL, "http://127.0.0.1:5000/")
    crl.setopt(crl.WRITEDATA, buffer)
    crl.perform()
    crl.close()
    response = buffer.getvalue()
    my_dictonary = dict(json.loads(response.decode("utf-8")))
    print(my_dictonary)

def test_data():
    """This is a test function for the API."""
    crl = pycurl.Curl()
    buffer = BytesIO()
    # buffer = StringIO()
    crl.setopt(crl.URL, "http://127.0.0.1:5000/predict")
    crl.setopt(crl.WRITEDATA, buffer)
    crl.perform()
    crl.close()
    response = buffer.getvalue()
    my_dictonary = dict(json.loads(response.decode("utf-8")))
    print(my_dictonary)

    """  my_result = requests.post(
        "http://127.0.0.1:5000/predict",
        params={
            "property-subtype": "CASTLE V",
            "living-area": "900N",
            "kitchen-type": "Hyper equipped",
            "swimming-pool": "true",
            "energy-class": "C_B",
            "street-address": "Rue Royale",
            "house-number": "190",
            "post-code": "1000",
        },
    )
    print(my_result.text)"""


if __name__ == "__main__":
    test_api()
    test_alive()
    test_data()
