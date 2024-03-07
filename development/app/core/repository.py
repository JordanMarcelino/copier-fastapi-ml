from typing import Any, Generic, TypeVar, Union
from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel, ValidationError
from sqlmodel import Session, SQLModel, select

Entity = TypeVar("Entity", bound=SQLModel)


class DatabaseRepository(Generic[Entity]):
    def __init__(self, model: type[Entity], session: Session) -> None:
        self.model = model
        self.session = session

    def get(self, pk: Union[UUID, int]) -> Entity:
        instance = self.session.get(self.model, pk)
        if instance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found!"
            )
        return instance

    def get_all(self) -> list[Entity]:
        instances = self.session.exec(select(self.model)).all()

        return instances

    def create(self, payload: BaseModel) -> Entity:
        try:
            instance = self.model.model_validate(payload)

            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)

            return instance
        except ValidationError as exc:
            self.session.rollback()

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unprocessable entity!",
            ) from exc

    def update(self, pk: Union[UUID, int], payload: BaseModel) -> Entity:
        try:
            instance = self.get(pk)

            payload_data = payload.model_dump(exclude_unset=True)
            for key, value in payload_data.items():
                setattr(instance, key, value)

            self.session.add(instance)
            self.session.commit()
            self.session.refresh(instance)

            return instance
        except ValidationError as exc:
            self.session.rollback()

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unprocessable entity!",
            ) from exc

    def delete(self, pk: Union[UUID, int]) -> None:
        instance = self.get(pk)

        self.session.delete(instance)
        self.session.commit()

    def filter_all(self, expression: dict[str, Any]) -> list[Entity]:
        statement = select(self.model)

        for key, value in expression.items():
            statement = statement.where(getattr(self.model, key) == value)

        instances = self.session.exec(statement).all()

        return instances

    def filter_one(self, expression: dict[str, Any]) -> Entity:
        statement = select(self.model)

        for key, value in expression.items():
            statement = statement.where(getattr(self.model, key) == value)

        instances = self.session.exec(statement).first()

        return instances
