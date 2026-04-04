from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    email: EmailStr | None = None
    age: int | None = Field(None, ge=0, le=150)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
