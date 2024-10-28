# tests/test_unit.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "name": "Test Item"}

def test_invalid_item():
    response = client.get("/items/999")
    assert response.status_code == 200
    assert "name" in response.json()