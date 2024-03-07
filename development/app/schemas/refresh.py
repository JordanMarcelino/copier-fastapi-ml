from uuid import uuid4

from sqlmodel import Field, SQLModel, Text, Uuid


class RefreshTokenBase(SQLModel):
    user_id: Uuid = Field(nullable=False)
    jti: Uuid = Field(nullable=False, index=True)
    refresh_token: Text = Field(nullable=False)


class RefreshToken(RefreshTokenBase, table=True):
    id: Uuid = Field(default=uuid4, nullable=False, primary_key=True)


class RefreshTokenCreate(RefreshTokenBase):
    pass
