from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_documents():
    response = client.get(
        "/documents"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        (dict, list),
    )


def test_delete_missing_document():
    response = client.delete(
        "/documents/non_existing_file.pdf"
    )

    assert response.status_code in [
        404,
        400,
    ]
