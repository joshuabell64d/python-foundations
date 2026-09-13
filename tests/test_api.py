from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_get_sample_project():
    response = client.get("/projects/PRJ-001")
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == "PRJ-001"
    assert data["evm_metrics"]["cost_variance"] == -30000.0


def test_evaluate_risk_valid():
    payload = {
        "risk_id": "R-999",
        "title": "Thruster test anomaly",
        "impact_score": 5,
        "likelihood_score": 3,
    }
    response = client.post("/risks/eval", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_score"] == 15


def test_evaluate_risk_invalid_impact():
    payload = {
        "risk_id": "R-999",
        "title": "Invalid impact test",
        "impact_score": 10,
        "likelihood_score": 3,
    }
    response = client.post("/risks/eval", json=payload)
    assert response.status_code == 422