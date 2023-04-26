import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
def test_category_create(auth_client, board_participant, user):
    url = reverse('todolist.goals:category-create')
    # board_new = BoardParticipant.objects.create(board=board, user=user, role=BoardParticipant.Role.owner)
    data = {'board': board_participant.board.id, 'title': 'тест', 'user': user.id, 'is_deleted': False}

    response = auth_client.post(url, data=data)

    expected = {'id': response.data["id"],
                "created": response.data["created"],
                "updated": response.data["updated"],
                'title': 'тест',
                'is_deleted': False, 'board': board_participant.board.id}

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected
