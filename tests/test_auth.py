from tests.conftest import client


def test_register():

    response = client.post(
        "/auth/register",
        json={
            "username": "pytest_user",
            "password": "123456"
        }
    )

    assert response.status_code in [200, 400]


def test_login():

    response = client.post(
        "/auth/login",
        json={
            "username": "pytest_user",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    assert "access_token" in response.json()