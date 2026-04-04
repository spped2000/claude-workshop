import pytest


@pytest.mark.asyncio
async def test_create_user_invalid_email(client):
    response = await client.post("/users", json={"name": "Alice", "email": "not-an-email", "age": 25})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_age_negative(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": -1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_age_too_high(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 151})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_empty_name(client):
    response = await client.post("/users", json={"name": "", "email": "alice@example.com", "age": 25})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_valid(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 25})
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_user_invalid_email(client):
    create = await client.post("/users", json={"name": "Bob", "email": "bob@example.com", "age": 30})
    user_id = create.json()["id"]
    response = await client.put(f"/users/{user_id}", json={"email": "bad-email"})
    assert response.status_code == 422
