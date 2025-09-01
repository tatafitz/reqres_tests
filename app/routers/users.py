from datetime import datetime
from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, paginate, add_pagination
from app.database import users
# from app.data import users_db
from app.models import UserResponse, UserCreate, User
from app.models.users import UserUpdate

router = APIRouter(prefix="/api/users")



@router.get("/{user_id}", response_model=UserResponse)
def get_single_user(user_id: int) -> UserResponse:
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
    return UserResponse(data=user)


@router.post("/", response_model=User, status_code=HTTPStatus.CREATED)
def create_user(user_data: UserCreate) -> User:
    """Создание нового пользователя"""
    # Создаем объект User без ID (будет назначен автоматически)
    user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        avatar=str(user_data.avatar)
    )
    return users.create_user(user)

    # name_parts = user.name.split()
    # first_name = name_parts[0]
    # last_name = name_parts[1] if len(name_parts) > 1 else ""
    #
    # # Создаем email из имени
    # email = f"{user.name.lower().replace(' ', '.')}@reqres.in"
    #
    # # Создаем URL аватара
    # avatar = f"https://reqres.in/img/faces/{len(users_db) + 1}-image.jpg"
    #
    # new_user = {
    #     "id": len(users_db) + 1,
    #     "email": email,
    #     "first_name": first_name,
    #     "last_name": last_name,
    #     "avatar": avatar,
    #     "name": user.name,
    #     "job": user.job,
    #     "createdAt": datetime.now(),
    #     "updatedAt": datetime.now()
    # }
    # users_db.append(new_user)
    # return User(**new_user)
#
#
@router.patch("/{user_id}", response_model=User, status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserCreate) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive number")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)
    # user_index = None
    # for current_user in users_db:
    #     if current_user["id"] == user_id:
    #         user_index = current_user
    #         break
    #
    # if not user_index:
    #     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    #
    # # Обновляем данные пользователя
    # updated_user = {
    #     **user_index,  # Копируем все существующие поля
    #     "name": user.name,
    #     "job": user.job,
    #     "updatedAt": datetime.now()
    # }
    #
    # # Находим индекс пользователя в списке для обновления
    # for i, current_user in enumerate(users_db):
    #     if current_user["id"] == user_id:
    #         users_db[i] = updated_user
    #         break
    #
    # return User(**updated_user)
#
#
@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    """Удаление пользователя"""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be a positive number")
    users.delete_user(user_id)
    return {"message":"User deleted"}

    # user_index = None
    # for current_user in users_db:
    #     if current_user["id"] == user_id:
    #         user_index = current_user
    #         break
    #
    # if not user_index:
    #     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    #
    # # Находим индекс пользователя в списке для удаления
    # for i, current_user in enumerate(users_db):
    #     if current_user["id"] == user_id:
    #         users_db.pop(i)
    #         break


@router.get("/", response_model=Page[User])
def list_users() -> Iterable[User]:
    """Получение списка пользователей с пагинацией"""
    return paginate(users.get_users())