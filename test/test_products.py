import os
import sys
from fastapi.testclient import TestClient
import main 
from main import app

client = TestClient(app)


def test_retreive_cars_403():
    response = client.get("/cars/", headers={"X-API-KEY": "CARS-TEST"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Unauthorized"}


def test_retreive_cars_200():
    response = client.get("/cars/?page=1&size=50", headers={"X-API-KEY": "cars-for-test"})
    assert response.status_code == 200



