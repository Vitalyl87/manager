import json
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from faker import Faker
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from main import main_app
from project_manager.base import Base
from project_manager.config import settings
from project_manager.db_helper import db_helper
from project_manager.project.models import Project
from project_manager.task.models import Task

fake = Faker("ru_RU")


@pytest_asyncio.fixture(scope="function")
async def async_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    async_engine = create_async_engine(settings.test.db, echo=False)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    conn = await async_engine.connect()
    try:
        yield conn
    except Exception:
        raise
    finally:
        await conn.rollback()
        await conn.close()

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_db_session(async_db_connection) -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_connection,
    )

    async with async_session() as session:

        await session.begin()
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_client(async_db_session) -> AsyncGenerator[AsyncClient, None]:
    def override_get_db():
        yield async_db_session

    main_app.dependency_overrides[db_helper.get_session] = override_get_db
    yield AsyncClient(transport=ASGITransport(app=main_app), base_url="http://test")
    del main_app.dependency_overrides[db_helper.get_session]


@pytest_asyncio.fixture(scope="function", autouse=True)
async def add_data_to_db(async_client) -> None:
    await async_client.post("/add_data/", params={"prj_count": 2, "task_count": 2})


@pytest.mark.asyncio
async def test_get_projects(async_client, async_db_session):
    response = await async_client.get("/projects/")
    client_data = response.json()
    db_data = await async_db_session.scalars(Select(Project).order_by(Project.id))
    expected_data = [{"name": x.name, "id": x.id} for x in db_data.all()]

    assert client_data == expected_data
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_tasks(async_client, async_db_session):
    response = await async_client.get("/tasks/")
    client_data = response.json()
    db_data = await async_db_session.scalars(Select(Task).order_by(Task.id))
    expected_data = [
        {"title": x.title, "status": x.status.value, "deadline": str(x.deadline)}
        for x in db_data.all()
    ]

    assert client_data == expected_data
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_task_by_project_id(async_client, async_db_session):
    project_id = 1
    response = await async_client.get(f"/tasks/{project_id}")
    client_data = response.json()

    db_data = await async_db_session.scalars(
        Select(Task).where(Task.project_id == project_id).order_by(Task.id)
    )
    expected_data = [
        {"title": x.title, "status": x.status.value, "deadline": str(x.deadline)}
        for x in db_data.all()
    ]

    assert client_data == expected_data
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_new_task(async_client, async_db_session):
    test_request_payload = {
        "title": fake.sentence(nb_words=3),
        "status": "new",
        "deadline": str(fake.date_this_year()),
        "project_id": 2,
    }

    response = await async_client.post(
        "/tasks/", content=json.dumps(test_request_payload)
    )
    client_data = response.json()
    expected = await async_db_session.get(Task, client_data["created_task_id"])

    assert response.status_code == 201
    assert test_request_payload["title"] == expected.title
    assert test_request_payload["status"] == expected.status.value
    assert test_request_payload["deadline"] == str(expected.deadline)
    assert test_request_payload["project_id"] == expected.project_id


@pytest.mark.asyncio
async def test_delete_task(async_client, async_db_session):
    task_id_to_delete = 1
    response = await async_client.delete(f"/tasks/{task_id_to_delete}")
    expected = await async_db_session.get(Task, task_id_to_delete)

    assert expected is None
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_patch_task(async_client, async_db_session):
    task_id_to_patch = 1
    new_status = "completed"
    response = await async_client.patch(
        f"/tasks/{task_id_to_patch}/status", params={"status": new_status}
    )
    expected = await async_db_session.get(Task, task_id_to_patch)

    assert expected.status.value == new_status
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_patch_task_bad_status(async_client):
    task_id_to_patch = 1
    new_status = "something_else"
    response = await async_client.patch(
        f"/tasks/{task_id_to_patch}/status", params={"status": new_status}
    )

    assert response.status_code == 422
