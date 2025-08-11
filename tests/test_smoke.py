import requests
from src.models.app_status import AppStatus

def test_server_available(base_url: str) -> None:
    """Тест доступности сервера"""
    response = requests.get(base_url)
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_status(base_url: str) -> None:
    """Тест получения статуса сервиса"""
    response = requests.get(f"{base_url}/status") 
    status = AppStatus.model_validate(response.json())
    assert status.users is True 