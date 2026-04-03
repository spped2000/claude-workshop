# Issue #106 | Group 6 — Add CORS configuration

## Context

Browser-based frontends (React, Vue, Svelte) cannot call the API unless the server includes
the correct CORS headers in responses. Without CORS configuration, every fetch from
`localhost:3000` will be blocked by the browser with a CORS error — even if the API is
running fine.

## Acceptance Criteria

- [ ] CORS is configured via `CORSMiddleware` from `fastapi.middleware.cors`
- [ ] Allowed origins: `http://localhost:3000` and `http://localhost:5173` (Vite default)
- [ ] Allowed methods: `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`
- [ ] Allowed headers: `Content-Type`, `Authorization`
- [ ] `allow_credentials` is set to `True`
- [ ] Middleware configuration is in `app/main.py`

## Test Requirements

- [ ] OPTIONS preflight request to `/users` returns 200
- [ ] Response to request from `http://localhost:3000` includes
  `Access-Control-Allow-Origin: http://localhost:3000`
- [ ] Request from an origin NOT in the allowed list does NOT receive the
  `Access-Control-Allow-Origin` header

## Hints for Claude

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
```

- `add_middleware` must be called **before** `app.include_router(...)` in `app/main.py`
- No new dependencies needed — `CORSMiddleware` is built into Starlette (installed with FastAPI)
- To test CORS headers in httpx, add an `Origin` header to the request:
  ```python
  response = await client.get("/users", headers={"Origin": "http://localhost:3000"})
  assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
  ```

## Definition of Done

A PR that passes all existing tests and includes new CORS tests,
referencing this issue as "Closes #106".
