import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
    AsyncConnection
)

from main import main_app
from project_manager.base import Base
from project_manager.config import settings
from project_manager.db_helper import dp_helper
from project_manager.project.models import Project
from project_manager.task.models import Task

ASYNC_DATABASE_URL = settings.test.db


@pytest_asyncio.fixture(scope="function")
async def async_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

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

    main_app.dependency_overrides[dp_helper.get_session] = override_get_db
    yield AsyncClient(transport=ASGITransport(app=main_app), base_url="http://test")
    del main_app.dependency_overrides[dp_helper.get_session]


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
