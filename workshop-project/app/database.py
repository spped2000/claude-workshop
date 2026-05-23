from typing import Any

users_db: dict[int, dict[str, Any]] = {}
_next_id: int = 1


def get_next_id() -> int:
    global _next_id
    current = _next_id
    _next_id += 1
    return current


def get_user(user_id: int) -> dict[str, Any] | None:
    user = users_db.get(user_id)
    if user is None or user.get("is_deleted"):
        return None
    return user


def create_user(data: dict[str, Any]) -> dict[str, Any]:
    user_id = get_next_id()
    user = {"id": user_id, "is_deleted": False, **data}
    users_db[user_id] = user
    return user


def update_user(user_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
    user = users_db.get(user_id)
    if user is None:
        return None
    user.update({k: v for k, v in data.items() if v is not None})
    return user


def delete_user(user_id: int) -> bool:
    user = users_db.get(user_id)
    if user is None or user.get("is_deleted"):
        return False
    user["is_deleted"] = True
    return True


def restore_user(user_id: int) -> dict[str, Any] | None:
    user = users_db.get(user_id)
    if user is None or not user.get("is_deleted"):
        return None
    user["is_deleted"] = False
    return user
