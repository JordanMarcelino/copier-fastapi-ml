from datetime import datetime
from typing import Annotated, Callable, Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.jwt import decode
from sqlmodel import Session, SQLModel

from app.core import DatabaseRepository, settings
from app.core.db import engine
from app.core.security import ALGORITHM, create_access_token
from app.entity.refresh import RefreshToken
from app.entity.user import Status, User
from app.schemas.auth import UserRead

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


async def check_refresh_token(
    request: Request,
    user_repository: Annotated[DatabaseRepository[User], Depends(get_repository(User))],
    refresh_repository: Annotated[
        DatabaseRepository[RefreshToken], Depends(get_repository(RefreshToken))
    ],
) -> None:
    try:
        access_token = request.headers.get("Authorization").split(" ")[1]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    decode_access_token = decode(
        access_token, settings.SECRET_KEY, algorithms=[ALGORITHM]
    )

    jti = decode_access_token["jti"]
    refresh_token = refresh_repository.filter_one({"jti": jti})

    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalid",
        )

    user = user_repository.get(decode_access_token["id"])
    if user.status == Status.INACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive",
        )

    decode_refresh_token = decode(
        refresh_token.refresh_token, settings.SECRET_KEY, algorithms=[ALGORITHM]
    )
    current_time = int(datetime.now().timestamp())

    if current_time >= decode_refresh_token["exp"]:
        refresh_repository.delete(refresh_token.id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalid",
        )

    if current_time >= decode_access_token["exp"]:
        access_token = create_access_token(
            user, jti, settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        request.headers["Authorization"] = access_token
