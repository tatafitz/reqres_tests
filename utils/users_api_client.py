from app.models.users import User
from config import Server
from utils.base_session import BaseSession


class UsersApiClient:
    """API клиент для работы с пользователями"""
    
    def __init__(self, **kwargs):
        env = kwargs.pop("env")
        self.session = BaseSession(base_url=Server(env).service_1)

    def fetch_user_by_id(self, user_id: int):
        """Получить пользователя по ID"""
        response = self.session.get(f"/api/users/{user_id}")
        return response

    def fetch_all_users(self):
        """Получить список всех пользователей"""
        response = self.session.get("/api/users/")
        return response

    def fetch_users_paginated(self, page: int = 1, size: int = 10):
        """Получить пользователей с пагинацией"""
        response = self.session.get("/api/users/", params={"page": page, "size": size})
        return response

    def create_new_user(self, user_data: dict):
        """Создать нового пользователя"""
        response = self.session.post("/api/users", json=user_data)
        return response

    def remove_user(self, user_id: int):
        """Удалить пользователя по ID"""
        response = self.session.delete(f"/api/users/{user_id}")
        return response

    def update_user_partial(self, user_id: int, update_data: dict):
        """Частично обновить данные пользователя (PATCH)"""
        response = self.session.patch(f"/api/users/{user_id}", json=update_data)
        return response
