"""Events App 配置类."""
from django.apps import AppConfig


class EventsConfig(AppConfig):
    """Events 应用配置."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "events"
    verbose_name = "事件管理"
