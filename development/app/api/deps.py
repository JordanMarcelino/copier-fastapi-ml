from typing import Annotated
from typing import Generator

from fastapi import Depends
from sqlmodel import Session

from app.core import engine


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
