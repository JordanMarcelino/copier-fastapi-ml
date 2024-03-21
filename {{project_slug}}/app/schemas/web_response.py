from typing import Any, Generic, List, Optional, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T")


class Info(BaseModel):
    status: bool = True
    meta: Any = None
    message: str


class WebResponse(Generic[T], BaseModel):
    info: Info
    data: Optional[Union[List[T], T]] = None
