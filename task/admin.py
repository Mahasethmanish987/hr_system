from django.contrib import admin
from .models import Task, SubTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "assigned_by",
        "assigned_to",
        "status",
        "priority",
        "due_date",
        "department",
        "created_at",
    )
    list_filter = ("status", "priority", "department", "due_date")
    search_fields = ("title", "description", "assigned_by__user__username", "assigned_to__user__username")
    ordering = ("-created_at",)
    date_hierarchy = "due_date"

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "parent_task",
        "assigned_by",
        "assigned_to",
        "status",
        "priority",
        "due_date",
        "department",
        "created_at",
    )
    list_filter = ("status", "priority", "department", "due_date")
    search_fields = (
        "title",
        "description",
        "parent_task__title",
        "assigned_by__user__username",
        "assigned_to__user__username",
    )
    ordering = ("-created_at",)
    date_hierarchy = "due_date"
