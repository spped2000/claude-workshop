# Workshop API — Project Context for Claude Code

## Project Overview

FastAPI REST API with in-memory user storage. Python 3.11+.

The API is **intentionally incomplete** — your assigned GitHub issue describes exactly what to add.

## Available MCP Servers

- **github**: Read issues, create branches, open pull requests
  - Key tools: `get_issue`, `create_branch`, `create_pull_request`, `search_code`

## Your Task (for each group)

1. Use the GitHub MCP to read your assigned issue number
2. Implement the feature described in the acceptance criteria
3. Write or update tests — all existing tests must continue to pass
4. Open a PR referencing the issue number (e.g. "Closes #1")

## Coding Conventions

- Use `async def` for all route handlers and test functions
- Pydantic v2 models live in `app/models.py`
- In-memory storage only — no database imports, no SQLAlchemy
- Add new routes to `app/routers/users.py` or directly to `app/main.py` (check your issue)
- Tests go in `tests/`, use `pytest-asyncio` with `httpx.AsyncClient`
- Add new dependencies to `requirements.txt` only if your issue explicitly requires one

## Project Structure

```
app/main.py           — FastAPI app, middleware registration, router mount
app/models.py         — All Pydantic request/response models
app/database.py       — In-memory dict storage + helper functions
app/routers/users.py  — User CRUD routes
tests/conftest.py     — Shared fixtures (auto-resets DB between tests)
tests/test_users.py   — Existing CRUD tests
```

## Test Pattern

```python
@pytest.mark.asyncio
async def test_example(client):  # client fixture from conftest.py
    response = await client.get("/some-endpoint")
    assert response.status_code == 200
```
