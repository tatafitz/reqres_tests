import pytest
import requests
from fastapi_pagination import Page

from app.models.users import User

test_users = [
    {
        "name": "George Bluth",
        "email": "george.bluth@reqres.in",
        "first_name": "George",
        "last_name": "Bluth",
        "avatar": "https://reqres.in/img/faces/default_image.jpg",
    },
    {
        "name": "Janet Weaver",
        "email": "janet.weaver@reqres.in",
        "first_name": "Janet",
        "last_name": "Weaver",
        "avatar": "https://reqres.in/img/faces/default_image.jpg",
    },
    {
        "name": "Emma Wong",
        "email": "emma.wong@reqres.in",
        "first_name": "Emma",
        "last_name": "Wong",
        "avatar": "https://reqres.in/img/faces/default_image.jpg",
    },
    {
        "name": "Eve Holt",
        "email": "eve.holt@reqres.in",
        "first_name": "Eve",
        "last_name": "Holt",
        "avatar": "https://reqres.in/img/faces/default_image.jpg",
    },
]


@pytest.mark.parametrize(
    "user_index", [0, 1, 2], ids=["random_user_1", "random_user_2", "random_user_3"]
)
def test_get_single_user(
    base_url: str, user_index: int, random_three_user_ids: list
) -> None:
    user_id = random_three_user_ids[user_index]
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 200
    user_response = User.model_validate(response.json())
    assert (
        user_response.id == user_id
    ), f"id пользователя не совпадает: ожидали {user_id}, получили {user_response.id}"


def test_get_single_user_not_found(base_url: str, users: Page[User]) -> None:
    """Проверка получения ошибки 404 при запросе несуществующего пользователя"""
    max_id = max(user.id for user in users.items)
    non_existent_id = max_id + 1

    response = requests.get(f"{base_url}/api/users/{non_existent_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


@pytest.mark.parametrize("user_id", [0, -1])
def test_get_single_user_negative_or_zero_id(base_url: str, user_id: int) -> None:
    """Проверка получения ошибки 422 при невалидном id пользователя"""
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 422
    assert response.json()["detail"] == "User ID must be a positive number"


@pytest.mark.parametrize("user_id", ["dsgjfh", "1aa"])
def test_get_single_user_string_id(base_url: str, user_id: str) -> None:
    """Проверка получения ошибки 422 при строковом id пользователя"""
    response = requests.get(f"{base_url}/api/users/{user_id}")

    assert response.status_code == 422
    error_detail = response.json()
    assert (
        "Input should be a valid integer, unable to parse string as an integer"
        in error_detail["detail"][0]["msg"]
    )


def test_users_no_duplicates(base_url: str, users) -> None:
    """Проверка отсутствия дубликатов id"""
    user_list = users.items
    assert len(user_list) == len({user.id for user in user_list})


@pytest.mark.parametrize("user_data", test_users[:2], ids=["user_1", "user_2"])
def test_create_user(base_url: str, user_data: dict, users: Page[User]) -> None:
    """Тест создания нового пользователя"""

    max_existing_id = max(user.id for user in users.items) if users.items else 0

    response = requests.post(f"{base_url}/api/users", json=user_data)

    assert response.status_code == 201
    created_user = User.model_validate(response.json())

    assert created_user.email == user_data["email"]
    assert created_user.first_name == user_data["first_name"]
    assert created_user.last_name == user_data["last_name"]
    assert created_user.avatar == user_data["avatar"]
    assert created_user.id is not None
    assert created_user.id > max_existing_id, (
        f"ID нового пользователя {created_user.id}"
        f" должен быть больше id последней записи {max_existing_id}"
    )
    requests.delete(f"{base_url}/api/users/{created_user.id}")


@pytest.mark.parametrize(
    "field_to_update,user_index",
    [("email", 0), ("first_name", 1), ("last_name", 2)],
    ids=["update_email", "update_first_name", "update_last_name"],
)
def test_update_user_patch(
    base_url: str, field_to_update: str, user_index: int, fill_test_data: list
) -> None:
    """Тест обновления пользователя с параметризацией"""
    user_id = fill_test_data[user_index]["id"]
    original_user_data = fill_test_data[user_index]
    original_value = original_user_data[field_to_update]
    update_data = {field_to_update: f"updated_{original_value}"}

    patch_response = requests.patch(f"{base_url}/api/users/{user_id}", json=update_data)

    User.model_validate(patch_response.json())
    assert patch_response.status_code == 200
    new_user_data = requests.get(f"{base_url}/api/users/{user_id}").json()

    expected_value = f"updated_{original_value}"
    assert new_user_data[field_to_update] == expected_value
    for field in ["email", "first_name", "last_name", "avatar"]:
        if field != field_to_update:
            assert new_user_data[field] == original_user_data[field]
    assert new_user_data["id"] == user_id


def test_delete_user(base_url: str, fill_test_data: list) -> None:
    """Тест удаления пользователя"""
    user_id = fill_test_data[-1]["id"]

    delete_response = requests.delete(f"{base_url}/api/users/{user_id}")
    get_response = requests.get(f"{base_url}/api/users/{user_id}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
