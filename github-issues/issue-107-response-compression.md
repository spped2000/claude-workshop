# Issue #107 | Group 7 — Add response compression

## Context

When `GET /users` returns hundreds of records, the JSON payload can be large. GZip
compression can reduce payload size by 60–80%, significantly improving response times over
slow connections. Starlette (which FastAPI uses internally) ships a `GZipMiddleware` that
handles this transparently.

## Acceptance Criteria

- [ ] GZip compression is enabled for all responses larger than 1000 bytes
- [ ] Compression uses `GZipMiddleware` from `fastapi.middleware.gzip`
- [ ] The minimum size threshold is defined as a constant `GZIP_MINIMUM_SIZE = 1000`
  at the top of `app/main.py`
- [ ] Existing endpoints continue to return correct JSON data
- [ ] Clients that do NOT send `Accept-Encoding: gzip` receive uncompressed responses

## Test Requirements

- [ ] `GET /users` with `Accept-Encoding: gzip` and a large user list (50+ users) returns
  a response with `Content-Encoding: gzip` header
- [ ] Small responses (under 1000 bytes) are NOT compressed — no `Content-Encoding` header
- [ ] All existing CRUD endpoints still return correct data after middleware is added

## Hints for Claude

```python
from fastapi.middleware.gzip import GZipMiddleware

GZIP_MINIMUM_SIZE = 1000

app.add_middleware(GZipMiddleware, minimum_size=GZIP_MINIMUM_SIZE)
```

- `GZipMiddleware` is part of Starlette — **no new pip package needed**
- Place `add_middleware` before `app.include_router(...)`
- To generate a large payload in tests, insert many users directly via `database.users_db`:
  ```python
  for i in range(50):
      database.users_db[i] = {"id": i, "name": f"User{i}", "email": f"u{i}@test.com", "age": 20}
  ```
- httpx `AsyncClient` auto-decompresses gzip by default. To check the header before
  decompression, inspect `response.headers.get("content-encoding")`

## Definition of Done

A PR that passes all existing tests and includes new compression tests,
referencing this issue as "Closes #107".
