import pytest


VALID_USER = {"name": "Alice", "email": "alice@example.com", "age": 30}


@pytest.mark.asyncio
async def test_post_invalid_email_returns_422(client):
    response = await client.post("/users", json={**VALID_USER, "email": "not-an-email"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_negative_age_returns_422(client):
    response = await client.post("/users", json={**VALID_USER, "age": -1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_age_over_150_returns_422(client):
    response = await client.post("/users", json={**VALID_USER, "age": 151})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_empty_name_returns_422(client):
    response = await client.post("/users", json={**VALID_USER, "name": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_valid_data_returns_201(client):
    response = await client.post("/users", json=VALID_USER)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["age"] == 30


@pytest.mark.asyncio
async def test_put_invalid_email_returns_422(client):
    await client.post("/users", json=VALID_USER)
    response = await client.put("/users/1", json={"email": "bad-email"})
    assert response.status_code == 422
