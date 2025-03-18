from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from typing import List, Optional
from .models import User, UserCreate, UserResponse, UserListResponse
from .models.app_status import AppStatus
from .data import users_db
from dotenv import load_dotenv
from fastapi_pagination import Page, paginate, add_pagination
import os

# Загружаем переменные окружения
load_dotenv()

app = FastAPI()

# Роуты
@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_single_user(user_id: int) -> UserResponse:
    """Получение информации о конкретном пользователе"""
    if user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User ID must be a positive number"
        )
    
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"data": user}

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> User:
    """Создание нового пользователя"""
    # Разбиваем имя на части
    name_parts = user.name.split()
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    
    # Создаем email из имени
    email = f"{user.name.lower().replace(' ', '.')}@reqres.in"
    
    # Создаем URL аватара
    avatar = f"https://reqres.in/img/faces/{len(users_db) + 1}-image.jpg"
    
    new_user = {
        "id": len(users_db) + 1,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "avatar": avatar,
        "name": user.name,
        "job": user.job,
        "createdAt": datetime.now(),
        "updatedAt": datetime.now()
    }
    users_db.append(new_user)
    return new_user

@app.put("/api/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserCreate) -> User:
    user_index = None
    for current_user in users_db:
        if current_user["id"] == user_id:
            user_index = current_user
            break
            
    if not user_index:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Обновляем данные пользователя
    updated_user = {
        **user_index,  # Копируем все существующие поля
        "name": user.name,
        "job": user.job,
        "updatedAt": datetime.now()
    }
    
    # Находим индекс пользователя в списке для обновления
    for i, current_user in enumerate(users_db):
        if current_user["id"] == user_id:
            users_db[i] = updated_user
            break
            
    return updated_user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Удаление пользователя"""
    user_index = None
    for current_user in users_db:
        if current_user["id"] == user_id:
            user_index = current_user
            break
            
    if not user_index:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Находим индекс пользователя в списке для удаления
    for i, current_user in enumerate(users_db):
        if current_user["id"] == user_id:
            users_db.pop(i)
            break

@app.get("/api/users", response_model=Page[User])
def list_users() -> Page[User]:
    """Получение списка пользователей с пагинацией"""
    return paginate(users_db)

@app.get("/status", response_model=AppStatus)
def status():
    return AppStatus(users=bool(users_db))

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/api/status", response_model=AppStatus)
def api_status():
    return AppStatus(users=bool(users_db))

# Добавляем пагинацию к приложению
add_pagination(app)