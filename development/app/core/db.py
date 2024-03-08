from sqlmodel import SQLModel, create_engine

from app.core import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
