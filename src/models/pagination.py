from fastapi_pagination import Page, Params
from typing import TypeVar, Generic, List

T = TypeVar("T")

class PaginatedResponse(Page[T], Generic[T]):
    class Config:
        from_attributes = True 