import json

import pytest
import os
import requests
from dotenv import load_dotenv
from pathlib import Path
import random

from fastapi_pagination import Page

from app.models import User

ENV_PATH = Path(__file__).parent.parent / ".env"

@pytest.fixture(autouse=True, scope="session")
def load_env():
    """Загрузка переменных окружения один раз за сессию тестов"""
    load_dotenv(ENV_PATH)

@pytest.fixture(scope="session")
def base_url():
    """Базовый URL для API"""
    return os.getenv("BASE_URL")

@pytest.fixture
def users(base_url) -> Page[User]:
    """Получение списка пользователей"""
    response = requests.get(f"{base_url}/api/users")
    data = response.json()
    return Page[User].model_validate(data)

@pytest.fixture(scope="session")
def fill_test_data(base_url):
    data_file_path = Path(__file__).parent.parent / "app" / "data.json"
    with open(data_file_path) as f:
        test_data_users = json.load(f)
        api_users = []
    for user in test_data_users:
        response = requests.post(f"{base_url}/api/users/", json=user)
        api_users.append(response.json())

    yield api_users

    for user in api_users:
        requests.delete(f"{base_url}/api/users/{user['id']}")

@pytest.fixture
def random_three_user_ids(fill_test_data):
    """Получение ID трех случайных пользователей из созданных тестовых данных"""

    created_users = fill_test_data
    
    if not created_users:
        return []

    valid_users = [user for user in created_users if user.get("id") is not None]

    if len(valid_users) <= 3:
        return [user["id"] for user in valid_users]

    random_users = random.sample(valid_users, 3)
    return [user["id"] for user in random_users]