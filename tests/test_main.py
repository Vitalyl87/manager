from fastapi.testclient import TestClient
from main import main_app
import pytest


def test_root_path():
    with TestClient(main_app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == "hello world"


def test_project_path():
    with TestClient(main_app) as client:
        response = client.get("/projects")
        assert response.status_code == 200
        assert type(response.json()) == list


def test_bad_path():
    with TestClient(main_app) as client:
        response = client.get("/dqdwq")
        assert response.status_code == 404


def test_task_path():
    with TestClient(main_app) as client:
        response = client.get("/tasks")
        assert response.status_code == 200
        assert type(response.json()) == list


def test_bad_task_path():
    with TestClient(main_app) as client:
        response = client.get("/tasks/xasxa")
        assert response.status_code != 200


if __name__ == "__main__":
    pytest.main()
