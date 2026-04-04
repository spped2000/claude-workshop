async def test_search_by_partial_name(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    await client.post("/users", json={"name": "Bob", "email": "bob@example.com", "age": 25})
    await client.post("/users", json={"name": "Charlie", "email": "charlie@example.com", "age": 35})

    response = await client.get("/users/search?q=lic")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Alice"
    assert data[0]["email"] == "alice@example.com"


async def test_search_by_partial_email(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    await client.post("/users", json={"name": "Bob", "email": "bob@example.com", "age": 25})

    response = await client.get("/users/search?q=example")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


async def test_search_case_insensitive(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})
    await client.post("/users", json={"name": "Bob", "email": "bob@example.com", "age": 25})

    response = await client.get("/users/search?q=alice")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Alice"


async def test_search_no_match_returns_empty(client):
    await client.post("/users", json={"name": "Alice", "email": "alice@example.com", "age": 30})

    response = await client.get("/users/search?q=nomatch")
    assert response.status_code == 200
    assert response.json() == []


async def test_search_missing_q_param_returns_422(client):
    response = await client.get("/users/search")
    assert response.status_code == 422
