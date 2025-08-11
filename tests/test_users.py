import pytest
import requests
from src.models.users import User, UserResponse
from src.data import users_db

# Тестовые данные
test_users = [
    {
        "id": 1,
        "name": "George Bluth",
        "job": "Developer",
        "email": "george.bluth@reqres.in",
        "first_name": "George",
        "last_name": "Bluth"
    },
    {
        "id": 2,
        "name": "Janet Weaver",
        "job": "Designer",
        "email": "janet.weaver@reqres.in",
        "first_name": "Janet",
        "last_name": "Weaver"
    },
    {
        "id": 3,
        "name": "Emma Wong",
        "job": "QA Engineer",
        "email": "emma.wong@reqres.in",
        "first_name": "Emma",
        "last_name": "Wong"
    }
]

@pytest.mark.parametrize("user", test_users)
def test_get_single_user(base_url: str, user: dict) -> None:
    """Тест получения информации о пользователе"""
    response = requests.get(f"{base_url}/api/users/{user['id']}")
    
    assert response.status_code == 200
    data = response.json()
    user_response = UserResponse.model_validate(data)
    assert user_response.data.id == user["id"]
    assert user_response.data.email == user["email"]
    assert user_response.data.first_name == user["first_name"]
    assert user_response.data.last_name == user["last_name"]

@pytest.mark.parametrize("user_id", [7])
def test_get_single_user_not_found(base_url: str, user_id: int) -> None:
    """Проверка получения ошибки 404 при запросе несуществующего пользователя"""
    response = requests.get(f"{base_url}/api/users/{user_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.parametrize("user_id", [0, -1, -5])
def test_get_single_user_negative_or_zero_id(base_url: str, user_id: int) -> None:
    """Проверка получения ошибки 422 при невалидном ID пользователя (отрицательные и ноль)"""
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 422
    error_detail = response.json()
    assert error_detail["detail"] == "User ID must be a positive number"

@pytest.mark.parametrize("user_id", ["dsgjfh", "abc", "123abc", ""])
def test_get_single_user_string_id(base_url: str, user_id: str) -> None:
    """Проверка получения ошибки 422 при строковом ID пользователя"""
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 422
    error_detail = response.json()
    assert isinstance(error_detail, dict)
    assert isinstance(error_detail.get("detail"), list)
    assert len(error_detail["detail"]) > 0
    assert "Input should be a valid integer, unable to parse string as an integer" in error_detail["detail"][0]["msg"]



def test_users_no_duplicates(base_url: str, users: dict) -> None:
    """Проверка отсутствия дубликатов в списке пользователей"""
    user_list = users["data"]
    assert len(user_list) == len(set(user["id"] for user in user_list))

@pytest.mark.parametrize("user_data", [
    {"name": "Иван Петров", "job": "QA инженер"},
    {"name": "Мария Сидорова", "job": "разработчик"},
    {"name": "Алексей Иванов", "job": "DevOps"}
])
def test_create_user(base_url: str, user_data: dict) -> None:
    """Тест создания нового пользователя"""
    response = requests.post(f"{base_url}/api/users", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    created_user = User.model_validate(data)
    assert created_user.name == user_data["name"]
    assert created_user.job == user_data["job"]
    assert created_user.id is not None
    assert created_user.createdAt is not None

@pytest.mark.parametrize("user,update_data", [
    (test_users[0], {"name": "George Updated", "job": "Senior Developer"}),
    (test_users[1], {"name": "Janet Updated", "job": "Senior Designer"}),
    (test_users[2], {"name": "Emma Updated", "job": "Senior QA"})
])
def test_update_user(base_url: str, user: dict, update_data: dict) -> None:
    """Тест обновления информации о пользователе"""
    response = requests.put(f"{base_url}/api/users/{user['id']}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    updated_user = User.model_validate(data)
    assert updated_user.name == update_data["name"]
    assert updated_user.job == update_data["job"]
    assert updated_user.updatedAt is not None

@pytest.mark.parametrize("user", test_users)
def test_delete_user(base_url: str, user: dict) -> None:
    """Тест удаления пользователя"""
    response = requests.delete(f"{base_url}/api/users/{user['id']}")
    assert response.status_code == 204