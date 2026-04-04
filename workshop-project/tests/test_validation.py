async def test_create_user_invalid_email(client):
    """POST /users with invalid email format returns 422"""
    response = await client.post("/users", json={"name": "Test", "email": "not-an-email", "age": 25})
    assert response.status_code == 422


async def test_create_user_negative_age(client):
    """POST /users with negative age returns 422"""
    response = await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": -1})
    assert response.status_code == 422


async def test_create_user_age_over_150(client):
    """POST /users with age over 150 returns 422"""
    response = await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": 151})
    assert response.status_code == 422


async def test_create_user_empty_name(client):
    """POST /users with empty name returns 422"""
    response = await client.post("/users", json={"name": "", "email": "test@example.com", "age": 25})
    assert response.status_code == 422


async def test_create_user_valid_data(client):
    """POST /users with valid data returns 201"""
    response = await client.post("/users", json={"name": "Valid User", "email": "valid@example.com", "age": 30})
    assert response.status_code == 201


async def test_update_user_invalid_email(client):
    """PUT /users/{id} with invalid email returns 422"""
    await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": 25})
    response = await client.put("/users/1", json={"email": "not-an-email"})
    assert response.status_code == 422


async def test_update_user_negative_age(client):
    """PUT /users/{id} with negative age returns 422"""
    await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": 25})
    response = await client.put("/users/1", json={"age": -5})
    assert response.status_code == 422


async def test_update_user_age_over_150(client):
    """PUT /users/{id} with age over 150 returns 422"""
    await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": 25})
    response = await client.put("/users/1", json={"age": 200})
    assert response.status_code == 422


async def test_update_user_empty_name(client):
    """PUT /users/{id} with empty name returns 422"""
    await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": 25})
    response = await client.put("/users/1", json={"name": ""})
    assert response.status_code == 422
