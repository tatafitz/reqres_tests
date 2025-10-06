import pytest

from utils.users_api_client import UsersApiClient


@pytest.fixture(scope='session')
def service_1(env):
    """Фикстура для API клиента пользователей"""
    api_client = UsersApiClient(env=env)
    yield api_client