import pytest
from app.core import settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.schemas.auth import User
from jose import jwt


@pytest.fixture(name="password")
def password_fixture() -> str:
    return "SECRET"


def test_hash_password_and_verify_success(password: str):
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) is True


def test_hash_password_and_verify_failed(password: str):
    hashed_password = get_password_hash(password)

    assert verify_password("dummy", hashed_password) is False


def test_create_access_token_success(password: str):
    access_token = create_access_token(
        User(email="test@gmail.com", password=password),
        "jti",
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["email"] == "test@gmail.com"
    assert payload["jti"] == "jti"
