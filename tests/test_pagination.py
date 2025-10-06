import math

import pytest
from fastapi_pagination import Page

from app.models import User


class TestPagination:
    @pytest.mark.parametrize(
        "page, size",
        [
            (1, 3),
            (2, 5),
            (1, 10),
            (3, 2),
        ],
    )
    def test_pagination_metadata_and_items_count(
        self, service_1, page: int, size: int, users: Page[User]
    ) -> None:
        """Тест для проверки page, size, total, pages и количества элементов при заданных page и size"""
        total_users = len(users.items)
        response = service_1.fetch_users_paginated(page=page, size=size)

        assert response.status_code == 200
        data = response.json()

        expected_pages = math.ceil(total_users / size)

        assert data["page"] == page
        assert data["size"] == size
        assert data["total"] == total_users
        assert data["pages"] == expected_pages

        start_index = (page - 1) * size
        end_index = min(page * size, total_users)
        expected_items_count = max(0, end_index - start_index)
        assert len(data["items"]) == expected_items_count

    @pytest.mark.parametrize("size", [1, 2, 3, 5, 10, 15])
    def test_pages_calculation_different_sizes(
        self, service_1, size: int, users: Page[User]
    ) -> None:
        """Тест для проверки pages при разных size"""
        total_users = len(users.items)
        response = service_1.fetch_users_paginated(page=1, size=size)

        assert response.status_code == 200
        data = response.json()

        expected_pages = math.ceil(total_users / size)
        assert data["pages"] == expected_pages

    def test_different_pages_return_different_data(self, service_1) -> None:
        """Тест, в котором возвращаются разные данные при разных значениях page"""
        size = 3

        response_page1 = service_1.fetch_users_paginated(page=1, size=size)
        response_page2 = service_1.fetch_users_paginated(page=2, size=size)

        assert response_page1.status_code == 200
        assert response_page2.status_code == 200

        data_page1 = response_page1.json()
        data_page2 = response_page2.json()

        ids_page1 = {item["id"] for item in data_page1["items"]}
        ids_page2 = {item["id"] for item in data_page2["items"]}

        assert not ids_page1.intersection(
            ids_page2
        ), "Страницы не должны содержать одинаковые элементы"

    def test_last_page_partial_fill(self, service_1, users: Page[User]) -> None:
        """Тест для проверки остатка на последней странице"""
        size = 3
        total_users = len(users.items)
        total_pages = math.ceil(total_users / size)

        if total_users % size == 0:
            pytest.skip("Последняя страница полностью заполнена")

        response = service_1.fetch_users_paginated(page=total_pages, size=size)

        assert response.status_code == 200
        data = response.json()

        expected_items_on_last_page = total_users % size
        assert len(data["items"]) == expected_items_on_last_page

    def test_empty_page_beyond_last(self, service_1, users: Page[User]) -> None:
        """Тест запроса страницы за пределами последней"""
        total_users = len(users.items)
        size = 3
        total_pages = math.ceil(total_users / size)
        empty_page = total_pages + 1

        response = service_1.fetch_users_paginated(page=empty_page, size=size)

        assert response.status_code == 200
        data = response.json()

        assert data["page"] == empty_page
        assert data["size"] == size
        assert data["total"] == total_users
        assert data["pages"] == total_pages
        assert len(data["items"]) == 0
