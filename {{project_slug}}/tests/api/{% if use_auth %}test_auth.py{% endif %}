import pytest
from app.core import settings
from fastapi.testclient import TestClient


@pytest.fixture(name="payload")
def payload_fixture() -> dict[str, str]:
    return {"email": "dummy@gmail.com", "password": "secret1@"}


def test_register_user_success(client: TestClient, payload: dict[str, str]) -> None:
    response = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)

    json = response.json()

    assert response.status_code == 200
    assert json["info"]["status"] is True
    assert json["info"]["message"] == "Success create user"
    assert json["data"]["email"] == payload["email"]


def test_register_user_failed_invalid_email(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["email"] = "wrong"

    response = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)

    json = response.json()

    assert response.status_code == 422
    assert json["info"]["status"] is False
    assert json["info"]["message"] == "Unprocessable entity"
    assert json["data"] is None


def test_register_user_failed_invalid_password_at_least_eight_character(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["email"] = "secr1@"

    response = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)

    json = response.json()

    assert response.status_code == 422
    assert json["info"]["status"] is False
    assert json["info"]["message"] == "Unprocessable entity"
    assert json["data"] is None


def test_register_user_failed_invalid_password_at_least_one_digit(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["email"] = "secrett@"

    response = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)

    json = response.json()

    assert response.status_code == 422
    assert json["info"]["status"] is False
    assert json["info"]["message"] == "Unprocessable entity"
    assert json["data"] is None


def test_register_user_failed_invalid_password_at_least_one_special_character(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["email"] = "secrett1"

    response = client.post(f"{settings.API_V1_STR}/auth/register", json=payload)

    json = response.json()

    assert response.status_code == 422
    assert json["info"]["status"] is False
    assert json["info"]["message"] == "Unprocessable entity"
    assert json["data"] is None


def test_login_user_success(client: TestClient, payload: dict[str, str]) -> None:
    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    json = response.json()

    assert response.status_code == 200
    assert json["info"]["status"] is True
    assert json["info"]["message"] == "Success login"
    assert json["data"]["token"] is not None


def test_login_user_failed_wrong_password(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["password"] = "wrong"

    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    json = response.json()

    assert response.status_code == 401
    assert json["info"]["status"] is False
    assert json["info"]["message"] == "Email or password is incorrect"
    assert json["data"] is None


def test_login_user_failed_wrong_email(
    client: TestClient, payload: dict[str, str]
) -> None:
    payload["email"] = "wrong"

    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    json = response.json()

    assert response.status_code == 422
    assert json["info"]["status"] is False
    assert json["info"]["message"] == "Unprocessable entity"
    assert json["data"] is None


def test_logout_user_success(client: TestClient, payload: dict[str, any]):
    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    json = response.json()
    access_token = json["data"]["token"]

    response = client.post(
        f"{settings.API_V1_STR}/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    json = response.json()

    assert response.status_code == 200
    assert json["info"]["status"] is True
    assert json["info"]["message"] == "Success logout"
    assert json["data"] is None


def test_profile_user_success(client: TestClient, payload: dict[str, any]):
    response = client.post(f"{settings.API_V1_STR}/auth/login", json=payload)

    json = response.json()
    access_token = json["data"]["token"]

    response = client.get(
        f"{settings.API_V1_STR}/auth/profile",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    json = response.json()

    assert response.status_code == 200
    assert json["info"]["status"] is True
    assert json["info"]["message"] == "Success get profile"
    assert json["data"]["email"] == payload["email"]
