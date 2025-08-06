from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_interpret_endpoint_mock():
    with open("tests/fixtures/dexcom_24h.json", "rb") as f:
        response = client.post(
            "/interpret",
            files={"file": ("dexcom_24h.json", f, "application/json")},
            data={"patient_id": "test-p", "provider_id": "test-doc"}
        )
    assert response.status_code == 200
    assert "interpretation_text" in response.json()
