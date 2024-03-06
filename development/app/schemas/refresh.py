from uuid import uuid4

from sqlmodel import Field
from sqlmodel import Uuid
from sqlmodel import Text
from sqlmodel import SQLModel


class RefreshToken(SQLModel, table=True):
    id: Uuid = Field(default=uuid4, nullable=False, primary_key=True)
    user_id: Uuid = Field(nullable=False)
    jti: Uuid = Field(nullable=False, index=True)
    refresh_token: Text = Field(nullable=False)
