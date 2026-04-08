import pytest


@pytest.mark.anyio
async def test_delete_returns_204_and_hides_user(client):
    # Create a user
    resp = await client.post("/users", json={"name": "Alice", "email": "a@b.com", "age": 30})
    user_id = resp.json()["id"]

    # Soft delete
    resp = await client.delete(f"/users/{user_id}")
    assert resp.status_code == 204

    # User no longer appears in list
    resp = await client.get("/users")
    assert resp.status_code == 200
    assert len(resp.json()) == 0


@pytest.mark.anyio
async def test_get_user_returns_404_after_soft_delete(client):
    resp = await client.post("/users", json={"name": "Alice", "email": "a@b.com", "age": 30})
    user_id = resp.json()["id"]

    await client.delete(f"/users/{user_id}")

    resp = await client.get(f"/users/{user_id}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_restore_returns_200_and_user_reappears(client):
    resp = await client.post("/users", json={"name": "Alice", "email": "a@b.com", "age": 30})
    user_id = resp.json()["id"]

    await client.delete(f"/users/{user_id}")

    # Restore
    resp = await client.post(f"/users/{user_id}/restore")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Alice"
    assert "is_deleted" not in resp.json()

    # User reappears in list
    resp = await client.get("/users")
    assert len(resp.json()) == 1


@pytest.mark.anyio
async def test_restore_non_deleted_user_returns_404(client):
    resp = await client.post("/users", json={"name": "Alice", "email": "a@b.com", "age": 30})
    user_id = resp.json()["id"]

    # Restore a non-deleted user
    resp = await client.post(f"/users/{user_id}/restore")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_restore_nonexistent_user_returns_404(client):
    resp = await client.post("/users/999/restore")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_list_users_returns_zero_after_delete(client):
    resp = await client.post("/users", json={"name": "Alice", "email": "a@b.com", "age": 30})
    await client.delete(f"/users/{resp.json()['id']}")

    resp = await client.get("/users")
    assert resp.json() == []


@pytest.mark.anyio
async def test_user_response_does_not_expose_is_deleted(client):
    resp = await client.post("/users", json={"name": "Alice", "email": "a@b.com", "age": 30})
    assert "is_deleted" not in resp.json()
