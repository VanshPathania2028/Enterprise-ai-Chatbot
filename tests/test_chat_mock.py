from api import routes
from auth.security import create_access_token
from tests.conftest import client


def test_chat_with_mocked_llm(monkeypatch):
    monkeypatch.setattr(routes, "hybrid_chat", lambda _: (
        "Artificial Intelligence is the simulation "
        "of human intelligence by machines."
    ))
    token = create_access_token({"sub": "pytest_user"})

    response = client.post(
        "/chat",
        json={
            "message": "What is Artificial Intelligence?"
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert len(data["response"]) > 0
