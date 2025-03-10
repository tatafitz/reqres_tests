from fastapi import FastAPI, HTTPException, status
from datetime import datetime
import random

from .models import UserCreate, User, UserResponse, UserListResponse
from .data import users_db

app = FastAPI()

# Роуты
@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user}

@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    new_user = {
        "id": len(users_db) + 1,
        "email": f"{user.name.lower().replace(' ', '.')}@reqres.in",
        "first_name": user.name.split()[0],
        "last_name": user.name.split()[1] if len(user.name.split()) > 1 else "",
        "avatar": f"https://reqres.in/img/faces/{random.randint(1, 12)}-image.jpg",
        "name": user.name,
        "job": user.job,
        "createdAt": datetime.now()
    }
    users_db.append(new_user)
    return new_user

@app.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Сохраняем все существующие поля
    existing_user = users_db[user_index]
    updated_user = {
        **existing_user,  # Копируем все существующие поля
        "name": user.name,
        "job": user.job,
        "updatedAt": datetime.now()
    }
    users_db[user_index] = updated_user
    return updated_user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    users_db.pop(user_index)
    return None

@app.get("/api/users", response_model=UserListResponse)
async def list_users(page: int = 1, per_page: int = 6):
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    total_pages = (len(users_db) + per_page - 1) // per_page
    
    return {
        "page": page,
        "per_page": per_page,
        "total": len(users_db),
        "total_pages": total_pages,
        "data": users_db[start_idx:end_idx]
    } 