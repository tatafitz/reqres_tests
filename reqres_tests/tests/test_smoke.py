import pytest
import requests
from reqres_tests.src.models.app_status import AppStatus

def test_server_available(base_url):
    """Тест доступности сервера"""
    response = requests.get(base_url)
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}

def test_status(base_url):
    """Тест получения статуса сервиса"""
    response = requests.get(f"{base_url}/api/status") 
    status = AppStatus.model_validate(response.json())
    assert status.users is True 