import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestRetrieveGoal:

    @pytest.fixture(autouse=True)
    def setup(self, goal):
        self.url = self.get_url(goal.id)

    @staticmethod
    def get_url(goal_pk: int) -> str:
        return reverse('todolist.goals:goal', kwargs={'pk': goal_pk})

    def test_owner_required(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_retrieve(self, auth_client, board_participant):
        auth_client.force_login(board_participant.user)
        response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
