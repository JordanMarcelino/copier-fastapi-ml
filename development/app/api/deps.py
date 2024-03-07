from typing import Annotated
from typing import Callable
from typing import Generator

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlmodel import Session
from sqlmodel import SQLModel

from app.core import DatabaseRepository
from app.core import settings
from app.core.db import engine
from app.core.security import ALGORITHM
from app.schemas.auth import User
from app.schemas.auth import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_repository(entity: type[SQLModel]) -> Callable[[Session], DatabaseRepository]:
    def func(session: SessionDep):
        return DatabaseRepository(entity, session)

    return func


async def get_current_user(
    repository: Annotated[DatabaseRepository, Depends(get_repository(User))],
    token: TokenDep,
) -> UserRead:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("id")
        user_db = repository.get(id)

        user_response = UserRead.model_validate(user_db, from_attributes=True)

        return user_response
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc
