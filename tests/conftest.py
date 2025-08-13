import pytest
import os
import requests
from dotenv import load_dotenv
from pathlib import Path


ENV_PATH = Path(__file__).parent.parent / ".env.example"

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

