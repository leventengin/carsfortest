
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_retreive_cars():
    response = client.get("/cars/", headers={"X-API-KEY": "CARS-TEST"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid X-Token header"}


