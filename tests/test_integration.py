from fastapi.testclient import TestClient

from auth.security import create_access_token
import main

app = main.app


client = TestClient(app)


def auth_headers():
    token = create_access_token({"sub": "pytest_user"})
    return {"Authorization": f"Bearer {token}"}


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data is not None


def test_chat_endpoint_valid_request(monkeypatch):
    monkeypatch.setattr(
        main,
        "rag_chat",
        lambda _: "Artificial intelligence is a field of computing.",
    )

    response = client.post(
        "/chat",
        json={
            "message": "What is artificial intelligence?"
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


def test_chat_endpoint_missing_message():
    response = client.post(
        "/chat",
        json={},
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_chat_endpoint_wrong_field():
    response = client.post(
        "/chat",
        json={
            "question": "What is AI?"
        },
        headers=auth_headers(),
    )

    assert response.status_code == 422
