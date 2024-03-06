from datetime import datetime
from datetime import timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(data: dict[str, Any], expires_delta: int) -> str:
    expire = datetime.now() + timedelta(minutes=expires_delta)
    data["exp"] = expire

    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
