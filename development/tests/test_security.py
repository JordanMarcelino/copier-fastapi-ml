import pytest
from jose import jwt

from app.core import settings
from app.core.security import ALGORITHM
from app.core.security import create_access_token
from app.core.security import get_password_hash
from app.core.security import verify_password


@pytest.fixture(name="password")
def generate_password() -> str:
    return "SECRET"


def test_hash_password_and_verify_success(password: str):
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) is True


def test_hash_password_and_verify_failed(password: str):
    hashed_password = get_password_hash(password)

    assert verify_password("dummy", hashed_password) is False


def test_create_access_token_success(password: str):
    access_token = create_access_token(
        {"password": password}, settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["password"] == password
