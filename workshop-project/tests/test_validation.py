async def test_post_user_invalid_email(client):
    """POST /users with invalid email returns 422"""
    response = await client.post("/users", json={"name": "Test", "email": "not-an-email", "age": 30})
    assert response.status_code == 422


async def test_post_user_age_too_low(client):
    """POST /users with age < 0 returns 422"""
    response = await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": -1})
    assert response.status_code == 422


async def test_post_user_age_too_high(client):
    """POST /users with age > 150 returns 422"""
    response = await client.post("/users", json={"name": "Test", "email": "test@example.com", "age": 151})
    assert response.status_code == 422


async def test_post_user_empty_name(client):
    """POST /users with empty name returns 422"""
    response = await client.post("/users", json={"name": "", "email": "test@example.com", "age": 30})
    assert response.status_code == 422


async def test_post_user_valid_data(client):
    """POST /users with valid data returns 201"""
    response = await client.post("/users", json={"name": "Test User", "email": "test@example.com", "age": 30})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["age"] == 30


async def test_put_user_invalid_email(client):
    """PUT /users/{id} with invalid email returns 422"""
    # First create a user
    await client.post("/users", json={"name": "Original", "email": "original@example.com", "age": 25})

    response = await client.put("/users/1", json={"email": "not-an-email"})
    assert response.status_code == 422


async def test_put_user_valid_email(client):
    """PUT /users/{id} with valid email should work"""
    # First create a user
    await client.post("/users", json={"name": "Original", "email": "original@example.com", "age": 25})

    response = await client.put("/users/1", json={"email": "new@example.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
