from fastapi.testclient import TestClient
from app import app
from unittest.mock import patch
from finding import BugFinding

client=TestClient(app)

def test_health_endpoint():
    response=client.get("/health")

    assert response.status_code==200
    assert response.json() == {
        "status":"healthy",
        "project":"Patchguard"
    }

def test_analyze_endpoint_returns_finding():
    fake_findings =[
        BugFinding(
             bug_type="missing_input_validation",
            function="withdraw",
            description="Negative amounts are not rejected.",
            severity="medium",
            verification_status="unverified"
        )
    ]

    with patch("app.analyze_code",return_value=fake_findings):
        response=client.post(
            "/analyze",
            json={
                "code": "def withdraw(balance, amount): return balance - amount"
            }
        )

    assert response.status_code==200

    data=response.json()
    assert len(data["findings"])==1
    assert data["findings"][0]["function"] == "withdraw"
    assert data["findings"][0]["severity"] == "medium"
    assert data["findings"][0]["verification_status"] == "unverified"

def test_analyze_endpoint_handles_analyzer_failure():
    with patch(
        "app.analyze_code",
        side_effect=ValueError("Invalide AI response")
    ):
        response=client.post(
            "/analyze",
            json={
                "code": "def example(): pass"
            }
        )

    assert response.status_code==502
    assert response.json()["detail"] == (
        "Code analysis failed. Check the AI service and response format."
    )