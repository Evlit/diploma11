import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import BoardParticipantFactory, GoalCategoryFactory


def test_root(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_admin(client):
    response = client.get('/admin/')
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db()
def test_board_auth_list(auth_client, user):
    BoardParticipantFactory.create_batch(5, user=user)
    url = reverse('todolist.goals:board-list')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db()
def test_board_list(client):
    url = reverse('todolist.goals:board-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
def test_category_auth_list(auth_client, board_participant):
    GoalCategoryFactory.create_batch(5, board=board_participant.board, user=board_participant.user)
    url = reverse('todolist.goals:category-list')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db()
def test_category_list(client):
    url = reverse('todolist.goals:category-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
def test_goal_auth_list(auth_client):
    url = reverse('todolist.goals:goal-list')
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_goal_list(client):
    url = reverse('todolist.goals:goal-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
