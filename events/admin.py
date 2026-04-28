"""Events Admin 配置."""
from django.contrib import admin

from .models import Attendee, Category, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类 Admin."""

    list_display = ["id", "name", "description", "created_at"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """事件 Admin."""

    list_display = ["id", "title", "category", "start_date", "end_date", "location"]
    list_filter = ["category", "start_date"]
    search_fields = ["title", "description", "location"]
    date_hierarchy = "start_date"
    ordering = ["-start_date"]


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    """参与者 Admin."""

    list_display = ["id", "name", "email", "event", "registration_date"]
    list_filter = ["event", "registration_date"]
    search_fields = ["name", "email"]
    ordering = ["-registration_date"]
