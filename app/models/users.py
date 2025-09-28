from pydantic import BaseModel, EmailStr, HttpUrl
from sqlmodel import Field, SQLModel


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


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl
