from fastapi import APIRouter, HTTPException
from app import database
from app.models import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.get("", response_model=list[UserResponse])
async def list_users():
    return [u for u in database.users_db.values() if not u.get("is_deleted")]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = database.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(body: UserCreate):
    user = database.create_user(body.model_dump())
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, body: UserUpdate):
    user = database.update_user(user_id, body.model_dump())
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    deleted = database.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/{user_id}/restore", response_model=UserResponse)
async def restore_user(user_id: int):
    user = database.restore_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
