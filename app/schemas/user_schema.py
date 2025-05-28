from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str
    profile_picture: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone_number: str
    profile_picture: Optional[str]
    is_blocked: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserWithToken(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
