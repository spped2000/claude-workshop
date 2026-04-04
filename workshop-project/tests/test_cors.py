import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


async def test_preflight_returns_200(client):
    response = await client.options(
        "/users",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200


async def test_allowed_origin_gets_cors_header(client):
    response = await client.get("/users", headers={"Origin": "http://localhost:3000"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


async def test_vite_origin_gets_cors_header(client):
    response = await client.get("/users", headers={"Origin": "http://localhost:5173"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


async def test_disallowed_origin_no_cors_header(client):
    response = await client.get("/users", headers={"Origin": "http://evil.example.com"})
    assert response.headers.get("access-control-allow-origin") is None
