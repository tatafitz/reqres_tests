from pydantic import BaseModel, EmailStr, HttpUrl
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel

if TYPE_CHECKING:
    # Для корректного type hinting в IDE
    pass
from typing import List, Optional, Dict, Any
from datetime import datetime
from .pagination import PaginatedResponse

class ConnectionStatus(BaseModel):
    database: bool

class UserBase(BaseModel):
    name: str
    job: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr
    first_name: str
    last_name: str
    avatar: str
    # createdAt: datetime
    # updatedAt: Optional[datetime] = None

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl

    
    def model_dump(self) -> Dict[str, Any]:
        """
        Serialize model to dict
        Совместимость с Pydantic v1 и v2
        """
        # Проверяем доступность метода
        if hasattr(super(), 'model_dump'):
            return super().model_dump()
        elif hasattr(self, 'dict'):
            return self.dict()
        else:
            return self.__dict__
    

#
# class UserResponse(BaseModel):
#     data: User

class UserListResponse(PaginatedResponse[User]):
    pass 