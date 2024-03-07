import pytest
from app.core import settings
from fastapi.testclient import TestClient


@pytest.fixture(name="payload")
def payload_fixture() -> dict[str, str]:
    return {"email": "dummy@gmail.com", "password": "secret"}


def test_register_user_success(client: TestClient, payload: dict[str, str]) -> None:

    response = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)

    user = response.json()

    assert response.status_code == 200
    assert user["info"]["status"] is True
    assert user["info"]["message"] == "Success create user"
    assert user["data"]["email"] == payload["email"]


def test_login_user_success(client: TestClient, payload: dict[str, str]) -> None:
    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    user = response.json()

    assert response.status_code == 200
    assert user["info"]["status"] is True
    assert user["info"]["message"] == "Success login"
    assert user["data"]["token"] is not None


def test_login_user_failed_wrong_password(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["password"] = "wrong"

    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    user = response.json()

    assert response.status_code == 401
    assert user["info"]["status"] is False
    assert user["info"]["message"] == "Email or password is incorrect"
    assert user["data"] is None


def test_login_user_failed_wrong_email(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["email"] = "wrong"

    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    user = response.json()

    assert response.status_code == 401
    assert user["info"]["status"] is False
    assert user["info"]["message"] == "Email or password is incorrect"
    assert user["data"] is None
