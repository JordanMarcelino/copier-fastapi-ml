from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Role(Enum):
    ADMIN = "admin"
    MEMBER = "member"


class User(SQLModel, table=True):
    email: str = Field(unique=True, index=True, nullable=False)
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    password: str = Field(nullable=False)
    status: Status = Field(default=Status.ACTIVE, nullable=False)
    role: Role = Field(default=Role.MEMBER, nullable=False)
    created_at: int = Field(
        default_factory=lambda: int(datetime.now().timestamp()), nullable=False
    )
