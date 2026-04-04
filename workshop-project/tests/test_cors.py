async def test_cors_preflight_request(client):
    """OPTIONS preflight request to /users returns 200 or 204"""
    response = await client.options("/users")
    assert response.status_code in [200, 204]


async def test_cors_origin_localhost_3000(client):
    """Response to request from localhost:3000 includes Access-Control-Allow-Origin header"""
    response = await client.get("/users", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    assert response.headers.get("access-control-allow-credentials") == "true"


async def test_cors_origin_localhost_5173(client):
    """Response to request from localhost:5173 includes Access-Control-Allow-Origin header"""
    response = await client.get("/users", headers={"Origin": "http://localhost:5173"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert response.headers.get("access-control-allow-credentials") == "true"


async def test_cors_disallowed_origin(client):
    """Request from disallowed origin does NOT receive Access-Control-Allow-Origin header"""
    response = await client.get("/users", headers={"Origin": "http://example.com"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") is None
