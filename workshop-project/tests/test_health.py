async def test_health_returns_200(client):
    response = await client.get("/health")
    assert response.status_code == 200


async def test_health_response_body(client):
    response = await client.get("/health")
    assert response.json() == {"status": "ok", "version": "1.0.0"}


async def test_health_works_with_empty_db(client):
    # DB is empty (reset by autouse fixture) — endpoint must still respond
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}
