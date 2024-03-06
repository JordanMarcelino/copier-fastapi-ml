from typing import Any
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

from pydantic import BaseModel


T = TypeVar("T")


class Info(BaseModel):
    status: bool = True
    meta: dict[str, Any] = None
    message: str


class WebResponse(Generic[T], BaseModel):
    data: Optional[Union[List[T], T]] = None
