from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.entity.user import Role, Status


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    status: Status
    role: Role
    created_at: int


class UserUpdate(UserBase):
    password: Optional[str] = None
    status: Optional[Status] = None
    role: Optional[Role] = None
