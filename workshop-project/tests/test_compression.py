from app import database


async def test_large_response_is_gzip_compressed(client):
    for i in range(50):
        database.users_db[i] = {"id": i, "name": f"User{i}", "email": f"u{i}@test.com", "age": 20}
    response = await client.get("/users", headers={"Accept-Encoding": "gzip"})
    assert response.status_code == 200
    assert response.headers.get("content-encoding") == "gzip"


async def test_small_response_is_not_compressed(client):
    response = await client.get("/users", headers={"Accept-Encoding": "gzip"})
    assert response.status_code == 200
    assert response.headers.get("content-encoding") is None


async def test_no_accept_encoding_no_compression(client):
    for i in range(50):
        database.users_db[i] = {"id": i, "name": f"User{i}", "email": f"u{i}@test.com", "age": 20}
    response = await client.get("/users", headers={"Accept-Encoding": "identity"})
    assert response.status_code == 200
    assert response.headers.get("content-encoding") is None


async def test_existing_crud_still_works(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"

    response = await client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"
