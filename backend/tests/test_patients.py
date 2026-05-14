import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_patients_returns_200():
    response = client.get("/api/patients/")
    assert response.status_code == 200


def test_list_patients_has_pagination():
    response = client.get("/api/patients/?limit=10&offset=0")
    data = response.json()
    assert "patients" in data
    assert "total" in data
    assert len(data["patients"]) <= 10


def test_filter_by_payer():
    response = client.get("/api/patients/?payer=Cigna")
    data = response.json()
    for p in data["patients"]:
        assert p["payer"] == "Cigna"


def test_filter_by_age_range():
    response = client.get("/api/patients/?min_age=30&max_age=40")
    data = response.json()
    for p in data["patients"]:
        assert 30 <= p["age"] <= 40
