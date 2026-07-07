import pytest

from app import create_app
from app.config import TestingConfig
from app.extensions import db


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.db"

    class LocalTestingConfig(TestingConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    app = create_app(LocalTestingConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_root_healthcheck(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Flask app is running"


def test_list_tasks_starts_empty(client) -> None:
    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task_success(client) -> None:
    response = client.post(
        "/api/tasks",
        json={"title": "Write tests", "description": "Cover CRUD endpoints."},
    )

    data = response.get_json()
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["title"] == "Write tests"
    assert data["description"] == "Cover CRUD endpoints."
    assert data["completed"] is False


def test_create_task_requires_non_empty_title(client) -> None:
    response = client.post("/api/tasks", json={"title": "   "})

    assert response.status_code == 400
    assert "title" in response.get_json()["error"]


def test_get_update_delete_task_flow(client) -> None:
    created = client.post("/api/tasks", json={"title": "Initial"}).get_json()
    task_id = created["id"]

    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["title"] == "Initial"

    update_response = client.patch(
        f"/api/tasks/{task_id}",
        json={"title": "Updated", "completed": True},
    )
    updated = update_response.get_json()
    assert update_response.status_code == 200
    assert updated["title"] == "Updated"
    assert updated["completed"] is True

    delete_response = client.delete(f"/api/tasks/{task_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/tasks/{task_id}")
    assert missing_response.status_code == 404
