from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_compare_route_with_valid_input():
    response = client.post(
        "/api/v1/compare",
        json={
            "model_name": "all-mpnet-base-v2",
            "sentences1": ["User access control"],
            "sentences2": ["Access control for users"],
        },
    )
    assert response.status_code == 200
    assert "similarity_scores" in response.json()
    assert isinstance(response.json()["similarity_scores"], list)
