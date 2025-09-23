from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate
from app.database import users
from app.models import UserCreate, User
from app.models.users import UserUpdate

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_single_user(user_id: int) -> User:
    """Получение информации о конкретном пользователе"""
    if user_id <= 0:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="User ID must be a positive number"
        )

    user = users.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=User, status_code=HTTPStatus.CREATED)
def create_user(user_data: UserCreate) -> User:
    """Создание нового пользователя"""
    user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        avatar=str(user_data.avatar)
    )
    return users.create_user(user)


@router.patch("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
def update_user(user_id: int, user_update: UserUpdate) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive number")
    return users.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    """Удаление пользователя"""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive number")
    users.delete_user(user_id)
    return {"message": "User deleted"}


@router.get("/", response_model=Page[User], status_code=HTTPStatus.OK)
def list_users() -> Page[User]:
    """Получение списка пользователей с пагинацией"""
    return paginate(users.get_users())
