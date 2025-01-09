import pytest
from httpx import ASGITransport, AsyncClient

from main import main_app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == "hello world"
