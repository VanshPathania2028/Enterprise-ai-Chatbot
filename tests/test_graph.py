from tests.conftest import client


def test_chat_requires_auth():

    response = client.post(
        "/chat",
        json={
            "message": "Hello"
        }
    )

    assert response.status_code in [401, 403]