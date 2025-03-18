from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from datetime import datetime
from .pagination import PaginatedResponse

class AppStatus(BaseModel):
    users: bool

class UserBase(BaseModel):
    name: str
    job: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    data: User

class UserListResponse(PaginatedResponse[User]):
    pass 