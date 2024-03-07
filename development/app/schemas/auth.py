import enum
from datetime import datetime
from typing import Optional
from uuid import UUID
from uuid import uuid4

from sqlmodel import BigInteger
from sqlmodel import Enum
from sqlmodel import Uuid
from sqlmodel import Field
from sqlmodel import SQLModel


class Status(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Role(enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, nullable=False)


class User(UserBase, table=True):
    id: Uuid = Field(default=uuid4, primary_key=True, nullable=False)
    password: str = Field(nullable=False)
    status: Enum = Field(default=Status.ACTIVE, nullable=False)
    role: Enum = Field(default=Role.MEMBER, nullable=False)
    created_at: BigInteger = Field(
        default=lambda _: int(datetime.now().timestamp()), nullabe=False
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
