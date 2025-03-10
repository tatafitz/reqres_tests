import pytest
import requests
from datetime import datetime

@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:8000"

@pytest.fixture(autouse=True)
def reset_db(base_url):
    """Сброс базы данных перед каждым тестом"""
    # Получаем список всех пользователей
    response = requests.get(f"{base_url}/api/users")
    users = response.json()["data"]
    
    # Удаляем всех пользователей кроме первых шести (начальных)
    for user in users[6:]:
        requests.delete(f"{base_url}/api/users/{user['id']}") 