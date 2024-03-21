import re
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core import PydanticCustomError

from app.entity.user import Role, Status


class UserBase(BaseModel):
    email: EmailStr


class UserLogin(UserBase):
    password: str


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        pattern = r"^(?=.*\d)(?=.*[!@#$%^&*()-_=+{};:,<.>?])(?=.*[a-zA-Z]).{8,}$"

        password_is_valid = bool(re.match(pattern, v))
        if not password_is_valid:
            raise PydanticCustomError(
                "value_error",
                "value is not a valid password. It must be at least 8 characters long, contain at least one digit, and contain at least one special character.",
                {
                    "reason": " Password must be at least 8 characters long, contain at least one digit, and contain at least one special character"
                },
            )

        return v


class UserRead(UserBase):
    id: UUID
    status: Status
    role: Role
    created_at: int


class UserUpdate(UserBase):
    password: Optional[str] = None
    status: Optional[Status] = None
    role: Optional[Role] = None
