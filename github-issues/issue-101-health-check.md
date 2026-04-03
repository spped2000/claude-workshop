# Issue #101 | Group 1 — Add health check endpoint

## Context

Load balancers, Kubernetes liveness probes, and uptime monitors all require a `/health`
endpoint that responds quickly without touching business logic. Without it, the platform
cannot verify the service is running.

## Acceptance Criteria

- [ ] `GET /health` returns HTTP 200
- [ ] Response body is exactly `{"status": "ok", "version": "1.0.0"}`
- [ ] Endpoint is defined directly in `app/main.py` (not in a router file)
- [ ] No database calls are made — response time should be under 50ms

## Test Requirements

- [ ] Test that `GET /health` returns 200
- [ ] Test that the response JSON matches `{"status": "ok", "version": "1.0.0"}` exactly
- [ ] Test that the endpoint works even when the users DB is empty

## Hints for Claude

- Use `@app.get("/health")` directly on the `app` object in `app/main.py`
- The version string `"1.0.0"` matches `app.version` set in the FastAPI constructor
- This requires zero new dependencies

## Definition of Done

A PR that passes all existing tests and includes new tests for the `/health` endpoint,
referencing this issue as "Closes #101".
