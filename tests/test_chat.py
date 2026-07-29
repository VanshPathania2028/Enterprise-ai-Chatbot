from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_chat_without_message():
    response = client.post(
        "/chat",
        json={},
    )

    assert response.status_code == 422


def test_chat_with_wrong_field():
    response = client.post(
        "/chat",
        json={
            "question": "What is AI?"
        },
    )

    assert response.status_code == 422


def test_chat_with_valid_message(monkeypatch):
    monkeypatch.setattr(
        main,
        "rag_chat",
        lambda _: "Artificial intelligence is a field of computing.",
    )

    response = client.post(
        "/chat",
        json={
            "message": "What is Artificial Intelligence?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        "response" in data
        or "answer" in data
    )
