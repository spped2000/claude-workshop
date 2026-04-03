import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app import database


@pytest.fixture(autouse=True)
def reset_db():
    database.users_db.clear()
    database._next_id = 1
    yield


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
