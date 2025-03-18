import pytest
import requests
from reqres_tests.src.models import User, UserResponse, UserListResponse
from reqres_tests.src.data import users_db

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
def test_get_single_user(base_url, user):
    """Тест получения информации о конкретном пользователе"""
    response = requests.get(f"{base_url}/api/users/{user['id']}")
    
    assert response.status_code == 200
    data = response.json()
    # Проверяем соответствие модели
    user_response = UserResponse.model_validate(data)
    assert user_response.data.id == user["id"]
    assert user_response.data.email == user["email"]
    assert user_response.data.first_name == user["first_name"]
    assert user_response.data.last_name == user["last_name"]

@pytest.mark.parametrize("user_id", [7])
def test_get_single_user_not_found(base_url, user_id):
    """Проверка получения ошибки 404 при запросе несуществующего пользователя"""
    response = requests.get(f"{base_url}/api/users/{user_id}")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.parametrize("user_id, expected_error", [
    (0, "User ID must be a positive number"),
    (-1, "User ID must be a positive number"),
    ("dsgjfh", "type_error")])
def test_get_single_user_invalid_id(base_url, user_id, expected_error):
    """Проверка получения ошибки 422 при невалидном ID пользователя"""
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 422

    if expected_error == "type_error":
        assert "input should be a valid integer" in response.json()["detail"][0]["msg"].lower()
    else:
        assert response.json()["detail"] == expected_error

@pytest.mark.parametrize("user_data", [
    {"name": "Иван Петров", "job": "QA инженер"},
    {"name": "Мария Сидорова", "job": "разработчик"},
    {"name": "Алексей Иванов", "job": "DevOps"}
])
def test_create_user(base_url, user_data):
    """Тест создания нового пользователя"""
    response = requests.post(f"{base_url}/api/users", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    # Проверяем соответствие модели
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
def test_update_user(base_url, user, update_data):
    """Тест обновления информации о пользователе"""
    response = requests.put(f"{base_url}/api/users/{user['id']}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    # Проверяем соответствие модели
    updated_user = User.model_validate(data)
    assert updated_user.name == update_data["name"]
    assert updated_user.job == update_data["job"]
    assert updated_user.updatedAt is not None

@pytest.mark.parametrize("page,size", [
    (1, 3),  # Первая страница, 3 элемента
    (2, 3),  # Вторая страница, 3 элемента
    (4, 3),  # Четвертая страница, 1 элемент
    (1, 5),  # Первая страница, 5 элементов
    (2, 5),  # Вторая страница, 5 элементов
])
def test_list_users_pagination(base_url, page, size):
    """Тест пагинации списка пользователей"""
    response = requests.get(f"{base_url}/api/users", params={"page": page, "size": size})
    assert response.status_code == 200
    
    data = response.json()
    total = len(users_db)
    total_pages = (total + size - 1) // size
    
    # Проверяем количество элементов на странице
    assert len(data["items"]) == (total - (page - 1) * size if page == total_pages else size)
    
    # Проверяем уникальность данных на странице
    assert len(data["items"]) == len(set(item["id"] for item in data["items"]))
    
    # Проверяем метаданные пагинации
    assert data["page"] == page
    assert data["size"] == size
    assert data["total"] == total  # Используем реальное количество пользователей
    assert data["pages"] == total_pages  # Правильное количество страниц
    
    # Проверяем, что данные на разных страницах разные
    if page > 1:
        prev_response = requests.get(f"{base_url}/api/users", params={"page": page - 1, "size": size})
        prev_data = prev_response.json()
        assert data["items"] != prev_data["items"]  # Данные должны отличаться

def test_list_users_empty_page(base_url):
    """Тест запроса страницы, на которой нет элементов"""
    total = len(users_db)
    size = 3
    empty_page = (total + size - 1) // size + 1  # Первая страница после последней
    
    response = requests.get(f"{base_url}/api/users", params={"page": empty_page, "size": size})
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["items"]) == 0  # Страница должна быть пустой
    assert data["page"] == empty_page
    assert data["size"] == size
    assert data["total"] == total
    assert data["pages"] == (total + size - 1) // size

def test_users_no_duplicates(base_url, users):
    """Проверка отсутствия дубликатов в списке пользователей"""
    user_list = users["data"]
    assert len(user_list) == len(set(user["id"] for user in user_list))

@pytest.mark.parametrize("user", test_users)
def test_delete_user(base_url, user):
    """Тест удаления пользователя"""
    response = requests.delete(f"{base_url}/api/users/{user['id']}")
    assert response.status_code == 204