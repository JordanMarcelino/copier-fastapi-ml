from sqlmodel import create_engine
from sqlmodel import SQLModel

from app.core import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
