import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import GoalCategory


@pytest.mark.django_db()
def test_goal_create(auth_client, board_participant,  user):
    url = reverse('todolist.goals:goal-create')
    category_new = GoalCategory.objects.create(board=board_participant.board, user=user)
    data = {"category": category_new.id, "title": "test goal"}

    response = auth_client.post(url, data=data)
    expected = {
        "id": response.data["id"],
        "title": "test goal",
        "category": category_new.id,
        "description": None,
        "due_date": None,
        "status": 1,
        "priority": 2,
        "created": response.data["created"],
        "updated": response.data["updated"],
    }

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected
