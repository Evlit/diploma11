from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.serializers import ProfileUserSerializer
from goals.models import GoalCategory, Goal


class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise ValidationError("Category is deleted")
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileUserSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise ValidationError("Category is deleted")
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value
