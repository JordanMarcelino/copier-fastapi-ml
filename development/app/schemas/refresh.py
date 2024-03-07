from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class RefreshTokenBase(SQLModel):
    user_id: UUID = Field(nullable=False)
    jti: UUID = Field(nullable=False, index=True)
    refresh_token: str = Field(nullable=False)


class RefreshToken(RefreshTokenBase, table=True):
    id: UUID = Field(default_factory=uuid4, nullable=False, primary_key=True)


class RefreshTokenCreate(RefreshTokenBase):
    pass
