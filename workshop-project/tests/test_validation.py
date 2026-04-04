async def test_create_user_invalid_email(client):
    response = await client.post("/users", json={"name": "Alice", "email": "not-an-email", "age": 30})
    assert response.status_code == 422


async def test_create_user_negative_age(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": -1})
    assert response.status_code == 422


async def test_create_user_age_too_high(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 151})
    assert response.status_code == 422


async def test_create_user_empty_name(client):
    response = await client.post("/users", json={"name": "", "email": "alice@example.com", "age": 30})
    assert response.status_code == 422


async def test_create_user_valid(client):
    response = await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["age"] == 30


async def test_update_user_invalid_email(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    response = await client.put("/users/1", json={"email": "not-an-email"})
    assert response.status_code == 422
