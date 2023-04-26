import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import GoalCategory, Goal


@pytest.mark.django_db()
def test_comment_create(auth_client,  board_participant,  user):
    url = reverse('todolist.goals:comment-create')
    category_new = GoalCategory.objects.create(board=board_participant.board, user=user)
    goal_new = Goal.objects.create(user=user, category_id=category_new.id)
    data = {"goal": goal_new.id, "text": "test comment"}

    response = auth_client.post(url, data=data)
    expected = {
        "id": response.data["id"],
        "text": "test comment",
        "goal": goal_new.id,
        "created": response.data["created"],
        "updated": response.data["updated"],
    }

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected
