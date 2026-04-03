# Issue #102 | Group 2 — Add request logging middleware

## Context

Without request logging, debugging production incidents is nearly impossible. Every request
should emit a structured log line that captures the HTTP method, path, response status code,
and how long the request took — so on-call engineers can trace slowdowns or errors.

## Acceptance Criteria

- [ ] Every request logs: HTTP method, path, response status code, and duration in milliseconds
- [ ] Logging uses Python's built-in `logging` module (no third-party logger like loguru)
- [ ] Middleware is registered in `app/main.py` using `@app.middleware("http")`
- [ ] Log level is `INFO`
- [ ] Log format example: `INFO:app.main:POST /users - 201 - 12ms`

## Test Requirements

- [ ] Test that a request to any endpoint produces a log entry (use `caplog` pytest fixture)
- [ ] Test that the log entry contains the HTTP method
- [ ] Test that the log entry contains the response status code
- [ ] Test that the duration value in the log is a positive number

## Hints for Claude

```python
import time, logging
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration_ms}ms")
    return response
```

- `request.method` gives the HTTP verb
- `request.url.path` gives the path (e.g. `/users`)
- `response.status_code` is available after `await call_next(request)`
- To capture logs in tests: use `@pytest.mark.asyncio` + `caplog` fixture

## Definition of Done

A PR that passes all existing tests and includes new tests verifying the log output,
referencing this issue as "Closes #102".
