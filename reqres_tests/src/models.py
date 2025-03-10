from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
    avatar: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    data: User

class UserListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[User] 