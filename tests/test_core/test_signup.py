import pytest
from django.urls import reverse
from rest_framework import status

from core.models import User
from tests.test_core.factories import SignUpRequest


@pytest.mark.django_db()
class TestSignupView:
    url = reverse('todolist.core:signup')

    def test_user_create(self, client):
        data = {'username': 'test_user', 'password': ',jh23;vB176', 'password_repeat': ',jh23;vB176'}

        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get()
        assert response.json() == _serialize_response(user)
        assert user.check_password(data['password'])

    def test_password_missmatch(self, client, faker):
        data = SignUpRequest.build(password_repeat=faker.password())
        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'password_repeat': ['Passwords']}

    @pytest.mark.parametrize('password', ['1234567890', 'q1w2e3', '123456qwerty'])
    def test_password_weak(self, client, password):
        data = SignUpRequest.build(password=password, password_repeat=password)
        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_exist(self, client, user):
        data = SignUpRequest.build(username=user.username)
        response = client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'username': ['Пользователь с таким именем уже существует.']}


def _serialize_response(user: User, **kwargs) -> dict:
    data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    data |= kwargs
    return data
