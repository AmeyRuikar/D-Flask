import json

import pytest
import car_app
from flask import Flask


@pytest.fixture
def app(mocker):
    # mocker.patch("car_app.car_info", return_value={})
    return car_app.app

def test_root_page(client):
    response = client.get("/")    
    assert response.status_code == 200

def test_car_info(client):
    response = client.get("/info")    
    assert response.status_code == 200
    assert response.json == car_app.car_info

def test_car_info_with_type(client):
    response = client.get("/info?type=sedan")    
    assert response.status_code == 200
    assert response.json == car_app.car_info['cars']['sedan']

def test_add_info_fails(client):
    # bad test
    headers = {'content-type': 'application/json'}
    data = {
                "name": "Escalade",
                "make": "Cadillac",
                "price": "90k"
            }
    response = client.post("/addInfo", data=json.dumps(data), headers=headers)    
    assert response.status_code == 500

def test_add_info(client):
    headers = {'content-type': 'application/json'}
    data = {
        	    "type": "suv",
                "name": "Escalade",
                "make": "Cadillac",
                "price": "90k"
            }
    response = client.post("/addInfo", data=json.dumps(data), headers=headers)    
    assert response.status_code == 200


def test_api_page(client):
    
    response = client.get("/apiMetadata")
    assert response.status_code == 200