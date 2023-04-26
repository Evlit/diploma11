import factory
from pytest_factoryboy import register

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return User.objects.create_user(*args, **kwargs)


class DateTimeMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True


@register
class BoardFactory(DateTimeMixin):
    title = factory.Faker('catch_phrase')

    class Meta:
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(DateTimeMixin):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


@register
class GoalCategoryFactory(DateTimeMixin):
    board = factory.SubFactory(BoardFactory)
    title = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalCategory


@register
class GoalFactory(DateTimeMixin):
    category = factory.SubFactory(GoalCategoryFactory)
    title = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Goal


@register
class GoalCommentFactory(DateTimeMixin):
    category = factory.SubFactory(GoalCategoryFactory)
    text = factory.Faker('catch_phrase')
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalComment
