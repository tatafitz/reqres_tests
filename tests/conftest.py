import json

import pytest
import os
import requests
from dotenv import load_dotenv
from pathlib import Path


ENV_PATH = Path(__file__).parent.parent / ".env"

@pytest.fixture(autouse=True)
def load_env():
    """Загрузка переменных окружения перед каждым тестом"""
    load_dotenv(ENV_PATH)

@pytest.fixture
def base_url():
    """Базовый URL для API"""
    return os.getenv("BASE_URL")

@pytest.fixture
def users(base_url):
    """Получение списка пользователей"""
    response = requests.get(f"{base_url}/api/users")
    return response.json()

@pytest.fixture
def fill_test_data(base_url):
    with open("app/data.json") as f:
        test_data_users = json.load(f)
        api_users = []
    for user in test_data_users:
        response = requests.post(f"{base_url}/api/users/", json=user)
        api_users.append(response.json())

    yield api_users  # Возвращаем созданных пользователей

    for user in api_users:
        requests.delete(f"{base_url}/api/users/{user['id']}")

@pytest.fixture
def random_three_user_ids(fill_test_data):
    """Получение ID трех случайных пользователей из созданных тестовых данных"""
    import random
    
    # fill_test_data возвращает список созданных пользователей
    created_users = fill_test_data
    
    if not created_users:
        return []
    
    # Проверяем, что у всех пользователей есть ID
    valid_users = [user for user in created_users if user.get("id") is not None]
    
    if not valid_users:
        return []
    
    # Если пользователей меньше или равно 3, возвращаем всех
    if len(valid_users) <= 3:
        return [user["id"] for user in valid_users]
    
    # Выбираем 3 случайных пользователя
    # Используем фиксированный seed для воспроизводимости (опционально)
    # random.seed(42)  # Раскомментируйте для детерминированных результатов
    random_users = random.sample(valid_users, 3)
    return [user["id"] for user in random_users]