async def test_options_preflight_returns_200(client):
    response = await client.options(
        "/users",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200


async def test_allowed_origin_receives_cors_header(client):
    response = await client.get("/users", headers={"Origin": "http://localhost:3000"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


async def test_vite_origin_receives_cors_header(client):
    response = await client.get("/users", headers={"Origin": "http://localhost:5173"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


async def test_disallowed_origin_no_cors_header(client):
    response = await client.get("/users", headers={"Origin": "http://evil.com"})
    assert response.headers.get("access-control-allow-origin") is None


async def test_credentials_allowed(client):
    response = await client.get("/users", headers={"Origin": "http://localhost:3000"})
    assert response.headers.get("access-control-allow-credentials") == "true"
