# Issue #103 | Group 3 — Add input validation for POST /users

## Context

Currently the API accepts any string as an email (including `"not-an-email"`), any integer
for age (including `-5` or `999`), and empty strings for name. This causes corrupt data
and confusing downstream errors. FastAPI + Pydantic v2 can enforce these constraints at
the model level with zero custom logic.

## Acceptance Criteria

- [ ] `email` field must be a valid email format — return HTTP 422 if not
- [ ] `age` must be between 0 and 150 inclusive — return HTTP 422 if outside range
- [ ] `name` must be at least 1 character — return HTTP 422 if empty string `""`
- [ ] The same validation applies to `PUT /users/{id}` when fields are provided
- [ ] Error responses follow FastAPI's default 422 Unprocessable Entity schema

## Test Requirements

- [ ] `POST /users` with `email: "not-an-email"` returns 422
- [ ] `POST /users` with `age: -1` returns 422
- [ ] `POST /users` with `age: 151` returns 422
- [ ] `POST /users` with `name: ""` returns 422
- [ ] `POST /users` with valid data still returns 201
- [ ] `PUT /users/{id}` with invalid email returns 422

## Hints for Claude

- Use `pydantic.EmailStr` for email validation:
  ```python
  from pydantic import BaseModel, EmailStr, Field
  email: EmailStr
  ```
- `EmailStr` requires the `email-validator` package: add `pydantic[email]` to `requirements.txt`
- Use `Field(ge=0, le=150)` for age range:
  ```python
  age: int = Field(..., ge=0, le=150)
  ```
- Use `Field(min_length=1)` for name:
  ```python
  name: str = Field(..., min_length=1)
  ```
- Modify `UserCreate` and `UserUpdate` models in `app/models.py`

## Definition of Done

A PR that passes all existing tests, adds `pydantic[email]` to `requirements.txt`,
and includes new validation tests, referencing this issue as "Closes #103".
