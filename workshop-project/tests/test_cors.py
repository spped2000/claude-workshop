import pytest


async def test_preflight_options_returns_200(client):
    response = await client.options(
        "/users",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200


async def test_allowed_origin_returns_cors_header(client):
    response = await client.get(
        "/users",
        headers={"Origin": "http://localhost:3000"},
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


async def test_disallowed_origin_no_cors_header(client):
    response = await client.get(
        "/users",
        headers={"Origin": "http://evil.com"},
    )
    assert "access-control-allow-origin" not in response.headers
