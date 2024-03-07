from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Role(Enum):
    ADMIN = "admin"
    MEMBER = "member"


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False)


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    password: str = Field(nullable=False)
    status: Status = Field(default=Status.ACTIVE, nullable=False)
    role: Role = Field(default=Role.MEMBER, nullable=False)
    created_at: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()), nullable=False
    )


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
