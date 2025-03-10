import pytest
import requests

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
    assert data["data"]["id"] == user["id"]
    assert data["data"]["email"] == user["email"]
    assert data["data"]["first_name"] == user["first_name"]
    assert data["data"]["last_name"] == user["last_name"]

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
    assert data["name"] == user_data["name"]
    assert data["job"] == user_data["job"]
    assert "id" in data
    assert "createdAt" in data

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
    assert data["name"] == update_data["name"]
    assert data["job"] == update_data["job"]
    assert "updatedAt" in data

@pytest.mark.parametrize("page,per_page", [
    (1, 3),
    (2, 3),
    (1, 6)
])
def test_list_users(base_url, page, per_page):
    """Тест получения списка пользователей с пагинацией"""
    response = requests.get(f"{base_url}/api/users", params={"page": page, "per_page": per_page})
    
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == page
    assert data["per_page"] == per_page
    assert "total" in data
    assert "total_pages" in data
    assert "data" in data
    assert len(data["data"]) <= per_page

@pytest.mark.parametrize("user", test_users)
def test_delete_user(base_url, user):
    """Тест удаления пользователя"""
    response = requests.delete(f"{base_url}/api/users/{user['id']}")
    assert response.status_code == 204 