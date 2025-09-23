import pytest
import requests
from fastapi_pagination import Page

from app.models.users import User, UserCreate

# Тестовые данные
test_users = [
    {
        "name": "George Bluth",
        "email": "george.bluth@reqres.in",
        "first_name": "George",
        "last_name": "Bluth",
        "avatar": "https://reqres.in/img/faces/default_image.jpg"
    },
    {
        "name": "Janet Weaver",
        "email": "janet.weaver@reqres.in",
        "first_name": "Janet",
        "last_name": "Weaver",
        "avatar": "https://reqres.in/img/faces/default_image.jpg"
    },
    {
        "name": "Emma Wong",
        "email": "emma.wong@reqres.in",
        "first_name": "Emma",
        "last_name": "Wong",
        "avatar": "https://reqres.in/img/faces/default_image.jpg"
    }
]

@pytest.mark.parametrize("user_index", [0, 1, 2], ids=["random_user_1", "random_user_2", "random_user_3"])
def test_get_single_user(base_url: str, user_index: int, random_three_user_ids: list) -> None:
    """Тест получения информации о пользователе из трех случайных созданных пользователей"""
    
    # Проверяем, что у нас есть достаточно пользователей для тестирования
    if len(random_three_user_ids) <= user_index:
        pytest.skip(f"Недостаточно пользователей для тестирования (нужен индекс {user_index}, доступно {len(random_three_user_ids)})")
    
    user_id = random_three_user_ids[user_index]
    response = requests.get(f"{base_url}/api/users/{user_id}")
    
    assert response.status_code == 200, f"Ошибка при получении пользователя с ID {user_id}"
    data = response.json()
    print('DATA', data)
    user_response = User.model_validate(data)
    assert user_response.id == user_id, f"ID пользователя не совпадает: ожидали {user_id}, получили {user_response.id}"

# @pytest.mark.parametrize("user_id", [7])
def test_get_single_user_not_found(base_url: str, users: Page[User]) -> None:
    """Проверка получения ошибки 404 при запросе несуществующего пользователя"""
    # Получаем ID последнего пользователя и прибавляем 1
    last_id = users.items[-1].id + 1
    
    response = requests.get(f"{base_url}/api/users/{last_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.parametrize("user_id", [0, -1, -5])
def test_get_single_user_negative_or_zero_id(base_url: str, user_id: int) -> None:
    """Проверка получения ошибки 422 при невалидном ID пользователя (отрицательные и ноль)"""
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 422
    error_detail = response.json()
    assert error_detail["detail"] == "User ID must be a positive number"

@pytest.mark.parametrize("user_id", ["dsgjfh", "1aa"])
def test_get_single_user_string_id(base_url: str, user_id: str) -> None:
    """Проверка получения ошибки 422 при строковом ID пользователя"""
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 422
    error_detail = response.json()
    assert isinstance(error_detail, dict)
    assert isinstance(error_detail.get("detail"), list)
    assert len(error_detail["detail"]) > 0
    assert "Input should be a valid integer, unable to parse string as an integer" in error_detail["detail"][0]["msg"]



def test_users_no_duplicates(base_url: str, users) -> None:
    """Проверка отсутствия дубликатов в списке пользователей"""
    user_list = users.items
    assert len(user_list) == len(set(user.id for user in user_list))

@pytest.mark.parametrize("user_data", test_users[:2], ids=["user_1", "user_2"])
def test_create_user(base_url: str, user_data: dict, users: Page[User]) -> None:
    """Тест создания нового пользователя"""
    # Получаем максимальный ID из существующих пользователей
    max_existing_id = max(user.id for user in users.items) if users.items else 0
    
    response = requests.post(f"{base_url}/api/users", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    created_user = User.model_validate(data)
    
    # Проверяем основные поля
    assert created_user.email == user_data["email"]
    assert created_user.first_name == user_data["first_name"]
    assert created_user.last_name == user_data["last_name"]
    assert created_user.avatar == user_data["avatar"]
    assert created_user.id is not None
    
    # Проверяем, что ID нового пользователя больше максимального существующего
    assert created_user.id > max_existing_id, f"ID нового пользователя ({created_user.id}) должен быть больше максимального существующего ({max_existing_id})"

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

def test_delete_user(base_url: str) -> None:
    """Тест удаления пользователя"""
    # Используем последний элемент из test_users для создания
    user_data = test_users[-1]
    
    # Сначала создаем пользователя
    create_response = requests.post(f"{base_url}/api/users", json=user_data)
    created_user_data = create_response.json()
    created_user = User.model_validate(created_user_data)
    
    # Теперь удаляем созданного пользователя
    delete_response = requests.delete(f"{base_url}/api/users/{created_user.id}")
    assert delete_response.status_code == 204
    
    # Проверяем, что пользователь действительно удален (запрос должен вернуть 404)
    get_response = requests.get(f"{base_url}/api/users/{created_user.id}")
    assert get_response.status_code == 404