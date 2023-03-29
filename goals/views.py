from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal
from goals.serializers import GoalCreateSerializer, GoalCategorySerializer, CategoryCreateSerializer, GoalSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [OrderingFilter, SearchFilter, ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted', ))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter,]
    filterset_class = GoalDateFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority"]
    ordering = ["priority", "due_date"]
    # ordering_fields = ["title", "created"]
    # ordering = ["title"]
    # search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
             ).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
             ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status', ))
