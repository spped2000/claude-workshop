from app import database


async def test_large_response_is_gzipped(client):
    for i in range(50):
        database.users_db[i] = {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
            "age": 20 + (i % 50),
        }

    response = await client.get("/users", headers={"Accept-Encoding": "gzip"})
    assert response.status_code == 200
    assert response.headers.get("content-encoding") == "gzip"
    assert len(response.json()) == 50


async def test_small_response_is_not_gzipped(client):
    response = await client.get("/users", headers={"Accept-Encoding": "gzip"})
    assert response.status_code == 200
    assert response.headers.get("content-encoding") is None
    assert response.json() == []


async def test_client_without_gzip_accept_gets_uncompressed(client):
    for i in range(50):
        database.users_db[i] = {
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com",
            "age": 20 + (i % 50),
        }

    response = await client.get("/users", headers={"Accept-Encoding": "identity"})
    assert response.status_code == 200
    assert response.headers.get("content-encoding") is None
    assert len(response.json()) == 50


async def test_existing_crud_still_works_after_middleware(client):
    create_resp = await client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com", "age": 30},
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Alice"

    put_resp = await client.put(f"/users/{user_id}", json={"name": "Alice Updated"})
    assert put_resp.status_code == 200
    assert put_resp.json()["name"] == "Alice Updated"

    delete_resp = await client.delete(f"/users/{user_id}")
    assert delete_resp.status_code == 204


async def test_health_endpoint_returns_correct_data(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}
