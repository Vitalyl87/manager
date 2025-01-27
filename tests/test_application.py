import json

import pytest
from httpx import ASGITransport, AsyncClient

from project_manager.main import main_app
from project_manager.task.crud import TaskCrud


def test_root_path(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == "hello world"


def test_project_path(test_app):
    response = test_app.get("/projects")
    assert response.status_code == 200


def test_bad_path(test_app):
    response = test_app.get("/dqdwq")
    assert response.status_code == 404


def test_task_path(test_app):
    response = test_app.get("/tasks")
    assert response.status_code == 200


def test_bad_task_path(test_app):
    response = test_app.get("/tasks/xasxa")
    assert response.status_code != 200


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == "hello world"


def test_get_task_by_project_id(test_app, monkeypatch):
    project_id = 5
    test_response_payload = [
        {"title": "string", "status": "new", "deadline": "2025-01-11"}
    ]

    async def mock_get(session, project_id):
        return [{"title": "string", "status": "new", "deadline": "2025-01-11"}]

    monkeypatch.setattr(TaskCrud, "get_task_by_project_id", mock_get)

    response = test_app.get(f"/tasks/{project_id}")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_get_task_by_project_id_and_status(test_app, monkeypatch):
    project_id = 5
    test_response_payload = [
        {"title": "string", "status": "new", "deadline": "2025-01-11"}
    ]

    async def mock_get(session, project_id, status):
        return [{"title": "string", "status": "new", "deadline": "2025-01-11"}]

    monkeypatch.setattr(TaskCrud, "get_task_by_project_id", mock_get)

    response = test_app.get(f"/tasks/{project_id}", params={"status": "new"})

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_create_task(test_app, monkeypatch):
    test_request_payload = {
        "title": "dqdwwqdw24",
        "status": "new",
        "deadline": "2025-01-11",
        "project_id": 2,
    }
    test_response_payload = {
        "message": "Task for project (id=2) added successfully",
        "created_task_id": 1,
    }

    async def mock_post(session, task):
        return 1

    monkeypatch.setattr(TaskCrud, "create_task_for_project_id", mock_post)

    response = test_app.post(
        "/tasks/",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_delete_task(test_app, monkeypatch):
    task_id = 5
    test_response_payload = {
        "message": f"Task with id={task_id} was deleted successfully"
    }

    async def mock_delete(session, id):
        return None

    monkeypatch.setattr(TaskCrud, "delete_by_id_or_404", mock_delete)

    response = test_app.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_patch_task(test_app, monkeypatch):
    task_id = 5
    test_response_payload = {
        "message": f"Task with id={task_id} was updated successfully"
    }

    async def mock_update(session, id, status):
        return None

    monkeypatch.setattr(TaskCrud, "patch_by_id_or_404", mock_update)
    response = test_app.patch(f"/tasks/{task_id}/status", params={"status": "new"})

    assert response.status_code == 200
    assert response.json() == test_response_payload


if __name__ == "__main__":
    pytest.main()
