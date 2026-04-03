# Issue #104 | Group 4 — Add soft delete for users

## Context

Hard deletes make data recovery impossible and break audit trails. Soft delete marks a user
as inactive while preserving the record, allowing recovery and historical queries. This is
standard practice in production systems.

## Acceptance Criteria

- [ ] `DELETE /users/{id}` now sets `is_deleted: true` instead of removing the record
- [ ] `GET /users` does NOT return soft-deleted users
- [ ] `GET /users/{id}` returns HTTP 404 for soft-deleted users (same as non-existent)
- [ ] A new `POST /users/{id}/restore` endpoint un-deletes a user (returns the user)
- [ ] `POST /users/{id}/restore` on a non-deleted or non-existent user returns 404
- [ ] The `UserResponse` model does NOT expose `is_deleted` (keep it internal storage only)

## Test Requirements

- [ ] `DELETE /users/{id}` returns 204 and the user no longer appears in `GET /users`
- [ ] `GET /users/{id}` returns 404 after soft delete
- [ ] `POST /users/{id}/restore` returns 200 and the user reappears in `GET /users`
- [ ] `POST /users/{id}/restore` on a non-deleted user returns 404
- [ ] Hard-deleted user count: `GET /users` still returns 0 after delete

## Hints for Claude

- Add `is_deleted: bool = False` to the initial user dict in `database.create_user()`
- Update `database.get_user()` to return `None` if `user["is_deleted"]` is `True`
- Update `database.delete_user()` to set `is_deleted = True` instead of `del users_db[user_id]`
- Add a new helper `database.restore_user(user_id)` that sets `is_deleted = False`
- For `GET /users`, filter: `[u for u in users_db.values() if not u.get("is_deleted")]`
- New route: `@router.post("/{user_id}/restore", response_model=UserResponse)`
- `UserResponse` in `app/models.py` should NOT include `is_deleted`

## Definition of Done

A PR that passes all existing tests and includes new soft-delete and restore tests,
referencing this issue as "Closes #104".
