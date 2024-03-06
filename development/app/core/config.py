import os
from secrets import token_urlsafe
from typing import Optional
from typing import Union

from pydantic import AnyHttpUrl
from pydantic import field_validator
from pydantic import ValidationInfo

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = token_urlsafe(32)

    # 60 minutes * 24 hours * 1 days = 1 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    # 60 minutes * 24 hours * 7 days = 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    BACKEND_CORS_ORIGINS: Union[list[AnyHttpUrl], str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list) or isinstance(v, str):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    # SQLModel Configuration
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", default="localhost")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> str:
        if isinstance(v, str):
            return v

        return f"postgresql://{info.data.get('POSTGRES_USER')}:{info.data.get('POSTGRES_PASSWORD')}@{info.data.get('POSTGRES_HOST')}:5432/{info.data.get('POSTGRES_DB')}?sslmode=disable"

    # TODO: Change env_file to .env
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env.dev")


settings = Settings()
