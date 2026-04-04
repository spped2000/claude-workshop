import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest.mark.asyncio
async def test_preflight_request(client):
    """OPTIONS preflight request to /users returns 204"""
    response = await client.options("/users", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 204
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


@pytest.mark.asyncio
async def test_cors_headers_allowed_origin(client):
    """Response to request from allowed origin includes CORS headers"""
    response = await client.get("/users", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    assert response.headers.get("access-control-allow-credentials") == "true"


@pytest.mark.asyncio
async def test_cors_headers_allowed_origin_vite(client):
    """Response to request from Vite origin includes CORS headers"""
    response = await client.get("/users", headers={"Origin": "http://localhost:5173"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert response.headers.get("access-control-allow-credentials") == "true"


@pytest.mark.asyncio
async def test_cors_headers_not_allowed_origin(client):
    """Request from non-allowed origin does NOT receive CORS headers"""
    response = await client.get("/users", headers={"Origin": "http://malicious.com"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") is None
