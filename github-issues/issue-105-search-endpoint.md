# Issue #105 | Group 5 — Add search endpoint GET /users/search

## Context

Fetching all users and filtering on the client side wastes bandwidth and is slow when there
are thousands of users. A server-side search endpoint lets clients find matching users
efficiently with a single query.

## Acceptance Criteria

- [ ] `GET /users/search?q=<query>` returns all users where `name` OR `email` contains the
  query string (case-insensitive, partial match)
- [ ] Returns an empty list `[]` (not 404) if no users match
- [ ] The query parameter `q` is required — missing `q` returns HTTP 422
- [ ] Search is performed in-memory (no external search engine)
- [ ] Response is a list of `UserResponse` objects

## Test Requirements

- [ ] Search by partial name returns matching users
- [ ] Search by partial email returns matching users
- [ ] Search is case-insensitive (`"alice"` matches `"Alice"`)
- [ ] No match returns `[]` with HTTP 200
- [ ] Missing `q` parameter returns 422

## Hints for Claude

> **CRITICAL:** The route `GET /users/search` must be declared **BEFORE** `GET /users/{user_id}`
> in `app/routers/users.py`. FastAPI matches routes in order — if `/{user_id}` comes first,
> the string `"search"` is treated as a user ID and you'll get a 422 or 404 instead.

```python
from fastapi import Query

@router.get("/search", response_model=list[UserResponse])
async def search_users(q: str = Query(...)):
    query = q.lower()
    results = [
        u for u in database.users_db.values()
        if query in u["name"].lower() or query in u["email"].lower()
    ]
    return results
```

- Place this route at the top of `app/routers/users.py`, before the `/{user_id}` route
- `Query(...)` means the parameter is required (raises 422 if missing)

## Definition of Done

A PR that passes all existing tests and includes new search tests,
referencing this issue as "Closes #105".
