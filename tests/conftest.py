import pytest
from rest_framework.test import APIClient

from core.models import User

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client


@pytest.fixture()
def another_user(user_factory) -> User:
    return user_factory.create()
