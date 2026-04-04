import pytest
from httpx import AsyncClient


async def test_post_invalid_email_returns_422(client: AsyncClient):
    response = await client.post("/users", json={"name": "Alice", "email": "not-an-email", "age": 25})
    assert response.status_code == 422


async def test_post_age_below_range_returns_422(client: AsyncClient):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": -1})
    assert response.status_code == 422


async def test_post_age_above_range_returns_422(client: AsyncClient):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 151})
    assert response.status_code == 422


async def test_post_empty_name_returns_422(client: AsyncClient):
    response = await client.post("/users", json={"name": "", "email": "alice@example.com", "age": 25})
    assert response.status_code == 422


async def test_post_valid_data_returns_201(client: AsyncClient):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 25})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["age"] == 25


async def test_put_invalid_email_returns_422(client: AsyncClient):
    create = await client.post("/users", json={"name": "Bob", "email": "bob@example.com", "age": 30})
    user_id = create.json()["id"]
    response = await client.put(f"/users/{user_id}", json={"email": "bad-email"})
    assert response.status_code == 422
