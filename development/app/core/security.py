from datetime import datetime
from datetime import timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core import settings
from app.schemas.auth import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(user: User, jti: str, expires_delta: int) -> str:
    to_encode = {}
    expire = datetime.now() + timedelta(minutes=expires_delta)

    to_encode["email"] = user.email
    to_encode["id"] = str(user.id)
    to_encode["jti"] = jti
    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
