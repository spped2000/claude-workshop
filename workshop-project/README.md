# Workshop API — Module 4: MCP & External Integrations

Base project for Lab 4.3 — GitHub Issue → PR workflow

## Quick Start

```bash
# Install dependencies
uv sync

# Run dev server
uv run uvicorn app.main:app --reload
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs

## Run Tests

```bash
uv run pytest
```

## Project Structure

```
app/
  main.py          — FastAPI app entry point
  models.py        — Pydantic request/response models
  database.py      — In-memory storage + helper functions
  routers/
    users.py       — User CRUD routes
tests/
  conftest.py      — Test fixtures (auto-resets DB between tests)
  test_users.py    — CRUD tests
```

## Available Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List all users |
| POST | /users | Create a user |
| GET | /users/{id} | Get a user |
| PUT | /users/{id} | Update a user |
| DELETE | /users/{id} | Delete a user |

## Your Task

1. Read your assigned GitHub issue using the GitHub MCP
2. Implement the feature following the acceptance criteria
3. Write tests in a separate file `tests/test_<feature>.py`
4. Create a PR referencing the issue number

```
Read issue #<your group's issue number> from spped2000/claude-workshop.
Implement the feature, write tests, and create a PR.
```
