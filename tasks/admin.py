from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tasks.models import TaskType, Position, Worker, Task
from django.contrib.auth.models import Group


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("position",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("position",)}),)
    list_display = UserAdmin.list_display + ("position",)
    search_fields = (
        "username",
        "position",
    )
    list_filter = (
        "username",
        "last_name",
        "position",
    )
    list_per_page = 20


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_completed",
        "task_type",
    )
    search_fields = (
        "name",
        "deadline",
        "task_type",
    )
    list_filter = (
        "name",
        "deadline",
        "is_completed",
        "task_type",
    )


admin.site.unregister(Group)

admin.site.register(TaskType)

admin.site.register(Position)
