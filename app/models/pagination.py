from fastapi_pagination import Page, Params
from typing import TypeVar, Generic, List
from pydantic import ConfigDict

T = TypeVar("T")

class PaginatedResponse(Page[T], Generic[T]):
    model_config = ConfigDict(from_attributes=True) 