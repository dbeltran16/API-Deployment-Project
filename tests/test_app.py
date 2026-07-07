from flask_app import app


def test_root_healthcheck() -> None:
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Flask app is running" in response.data
