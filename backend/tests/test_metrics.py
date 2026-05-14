import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_returns_200():
    response = client.get("/api/metrics/dashboard")
    assert response.status_code == 200


def test_dashboard_has_required_fields():
    response = client.get("/api/metrics/dashboard")
    data = response.json()
    assert "overall_compliance" in data
    assert "total_patients" in data
    assert "summaries" in data
    assert isinstance(data["summaries"], list)


def test_summaries_have_rate():
    response = client.get("/api/metrics/dashboard")
    for s in response.json()["summaries"]:
        assert "compliance_rate" in s
        assert 0 <= float(s["compliance_rate"]) <= 100
