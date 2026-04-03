from typing import Any

users_db: dict[int, dict[str, Any]] = {}
_next_id: int = 1


def get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


def get_user(user_id: int) -> dict[str, Any] | None:
    return users_db.get(user_id)


def create_user(data: dict[str, Any]) -> dict[str, Any]:
    user_id = get_next_id()
    user = {"id": user_id, **data}
    users_db[user_id] = user
    return user


def update_user(user_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
    user = users_db.get(user_id)
    if user is None:
        return None
    user.update({k: v for k, v in data.items() if v is not None})
    return user


def delete_user(user_id: int) -> bool:
    if user_id not in users_db:
        return False
    del users_db[user_id]
    return True
