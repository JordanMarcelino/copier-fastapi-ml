from datetime import datetime
from typing import Annotated, Callable, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, SQLModel

from app.core import DatabaseRepository, settings
from app.core.db import engine
from app.core.security import ALGORITHM
from app.schemas.auth import User, UserRead

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT"
)


def get_session() -> Generator[Session, None, None]:
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

        user_id = payload.get("id")
        user_db = repository.get(user_id)

        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_response = UserRead.model_validate(**user_db.model_dump())

        return user_response
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
