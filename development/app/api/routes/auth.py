from typing import Annotated, Any
from uuid import uuid4

from fastapi import Depends, Request, status
from fastapi.routing import APIRouter, HTTPException
from jose.jwt import decode

from app.api.deps import get_repository
from app.core import settings
from app.core.repository import DatabaseRepository
from app.core.security import (
    ALGORITHM,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.entity.refresh import RefreshToken, RefreshTokenCreate
from app.entity.user import User
from app.schemas.auth import UserCreate, UserRead
from app.schemas.web_response import Info, WebResponse

router = APIRouter(prefix="/auth", tags=["auth"])

UserRepository = Annotated[DatabaseRepository[User], Depends(get_repository(User))]
RefreshRepository = Annotated[
    DatabaseRepository[RefreshToken], Depends(get_repository(RefreshToken))
]


@router.post("/login")
def login(
    user_repository: UserRepository,
    refresh_repository: RefreshRepository,
    user_in: UserCreate,
):
    user = user_repository.filter_one({"email": user_in.email})

    if user is None or not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
        )

    jti = uuid4()
    access_token = create_access_token(
        user, str(jti), settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_access_token(
        user, str(jti), settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    refresh_repository.create(
        RefreshTokenCreate(user_id=user.id, jti=jti, refresh_token=refresh_token)
    )

    return WebResponse[dict[str, str]](
        info=Info(message="Success login"), data={"token": access_token}
    )


@router.post("/register", response_model=WebResponse)
def register(repository: UserRepository, user_in: UserCreate) -> Any:
    hashed_password = get_password_hash(user_in.password)
    setattr(user_in, "password", hashed_password)

    user = repository.create(user_in)

    return WebResponse[UserRead](
        info=Info(message="Success create user"),
        data=UserRead(**user.model_dump()),
    )


@router.post("/logout", response_model=WebResponse)
def logout(request: Request, repository: RefreshRepository) -> Any:
    access_token = request.headers.get("Authorization").split(" ")[1]
    payload = decode(access_token, settings.SECRET_KEY, algorithms=[ALGORITHM])

    refresh = repository.filter_one({"jti": payload["jti"]})
    repository.delete(refresh.id)

    return WebResponse[None](info=Info(message="Success logout"))
