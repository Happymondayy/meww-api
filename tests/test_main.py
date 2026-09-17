from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_echo():
    payload = {"title": "노르웨이의 숲", "creator": "무라카미 하루키", "rating": 5}
    response = client.post("/echo", json=payload)
    assert response.status_code == 200
    assert response.json() == payload