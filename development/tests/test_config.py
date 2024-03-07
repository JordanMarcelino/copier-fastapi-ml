from app.core import settings


# TODO: Add test config after generate template
def test_configuration() -> None:
    assert settings.API_V1_STR == "/api/v1"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60 * 24 * 1
    assert settings.BACKEND_CORS_ORIGINS is not None
