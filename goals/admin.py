from django.contrib import admin
from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority')


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'text')
    search_fields = ('user', 'goal')
    list_filter = ('user',)


# admin.site.register(BoardParticipant)
@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'board')
    search_fields = ('user', 'role')
    list_filter = ('user',)
