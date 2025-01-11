import pytest


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


if __name__ == "__main__":
    pytest.main()
