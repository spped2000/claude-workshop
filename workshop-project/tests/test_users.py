import pytest


@pytest.mark.asyncio
async def test_list_users_empty(client):
    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["age"] == 30


@pytest.mark.asyncio
async def test_list_users_after_create(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    await client.post("/users", json={"name": "Bob", "email": "bob@example.com", "age": 25})
    response = await client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_user(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    response = await client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    response = await client.put("/users/1", json={"name": "Alice Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Updated"
    assert response.json()["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_update_user_not_found(client):
    response = await client.put("/users/999", json={"name": "Ghost"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    response = await client.delete("/users/1")
    assert response.status_code == 204
    get_response = await client.get("/users/1")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_user_not_found(client):
    response = await client.delete("/users/999")
    assert response.status_code == 404
