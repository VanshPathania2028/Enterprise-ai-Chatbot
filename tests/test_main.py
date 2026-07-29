from tests.conftest import client


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Enterprise AI Chatbot API"
    assert data["version"] == "1.0.0"
