import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_results_latest():
    resp = client.get("/results/latest")
    assert resp.status_code == 200
    assert isinstance(resp.json(), (dict, list))

def test_trigger():
    resp = client.post("/trigger")
    assert resp.status_code == 200
    assert "status" in resp.json()

def test_results_query():
    resp = client.get("/results/query")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
