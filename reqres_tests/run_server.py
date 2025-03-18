import uvicorn
import json
from datetime import datetime
from src.models import User
from src.data import users_db
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

def load_and_validate_users():
    """Загрузка и валидация пользователей из JSON файла"""
    db_path = os.getenv("DB_PATH", "data.json")
    with open(db_path, "r") as f:
        users_data = json.load(f)
    
    # Очищаем текущую базу данных
    users_db.clear()
    
    # Валидируем и добавляем каждого пользователя
    for user_data in users_data:
        # Преобразуем строку даты в объект datetime
        if isinstance(user_data.get("createdAt"), str):
            user_data["createdAt"] = datetime.fromisoformat(user_data["createdAt"])
        
        # Валидируем данные через Pydantic модель
        user = User.model_validate(user_data)
        users_db.append(user.model_dump())
    
    print(f"Успешно загружено {len(users_db)} пользователей")

if __name__ == "__main__":
    load_and_validate_users()
    
    # Получаем настройки из переменных окружения
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    host = base_url.split("://")[1].split(":")[0]
    port = int(base_url.split(":")[-1])
    
    uvicorn.run("src.api:app", host=host, port=port, reload=True) 