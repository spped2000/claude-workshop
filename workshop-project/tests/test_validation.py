"""Tests for input validation on POST /users and PUT /users/{id}."""

import pytest
from httpx import AsyncClient


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


@pytest.mark.asyncio
async def test_put_empty_name_returns_422(client):
    await client.post("/users", json=VALID_USER)
    response = await client.put("/users/1", json={"name": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_put_negative_age_returns_422(client):
    await client.post("/users", json=VALID_USER)
    response = await client.put("/users/1", json={"age": -1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_put_over_150_age_returns_422(client):
    await client.post("/users", json=VALID_USER)
    response = await client.put("/users/1", json={"age": 151})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_put_valid_update_returns_200(client):
    await client.post("/users", json=VALID_USER)
    response = await client.put("/users/1", json={"name": "Bob", "email": "bob@example.com", "age": 40})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Bob"
    assert data["email"] == "bob@example.com"
    assert data["age"] == 40


@pytest.mark.asyncio
async def test_post_age_at_boundary_0(client):
    response = await client.post("/users", json={**VALID_USER, "age": 0})
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_post_age_at_boundary_150(client):
    response = await client.post("/users", json={**VALID_USER, "age": 150})
    assert response.status_code == 201
