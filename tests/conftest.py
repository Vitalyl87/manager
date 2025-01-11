import pytest
from fastapi.testclient import TestClient

from main import main_app


@pytest.fixture(scope="function")
def test_app():
    with TestClient(main_app) as client:
        yield client
