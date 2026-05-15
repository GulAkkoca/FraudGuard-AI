from fastapi.testclient import TestClient

from main import app


def test_analyze_demo_endpoint():
    client = TestClient(app)
    response = client.post("/analyze-demo/p003")

    assert response.status_code == 200
    assert response.json()["product"]["id"] == "p003"

