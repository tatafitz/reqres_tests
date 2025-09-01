import requests
from app.models.app_status import AppStatus
from typing import TypeVar, Type
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

def validate_model(model_class: Type[T], data: dict) -> T:
    """Универсальная функция для валидации моделей, совместимая с Pydantic v1/v2"""
    try:
        # Pydantic v2
        return model_class.model_validate(data)
    except AttributeError:
        # Pydantic v1
        return model_class.parse_obj(data)

def test_server_available(base_url: str) -> None:
    """Тест доступности сервера"""
    response = requests.get(base_url)
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_status(base_url: str) -> None:
    """Тест получения статуса сервиса"""
    response = requests.get(f"{base_url}/status") 
    status = validate_model(AppStatus, response.json())
    assert status.users is True 