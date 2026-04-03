# Workshop API — Module 4: MCP & External Integrations

Base project สำหรับ Lab 4.3 — GitHub Issue → PR workflow

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API จะอยู่ที่ http://localhost:8000
Docs อยู่ที่ http://localhost:8000/docs

## Run Tests

```bash
pytest
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

1. ดู GitHub issue ที่ได้รับมอบหมายโดยใช้ GitHub MCP
2. Implement feature ตาม acceptance criteria ใน issue
3. เขียน tests
4. สร้าง PR

```
Read issue #<หมายเลข issue ของกลุ่มคุณ> from this repo.
Implement the feature, write tests, and create a PR.
```
