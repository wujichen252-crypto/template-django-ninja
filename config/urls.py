"""URL 配置文件."""
from django.contrib import admin
from django.urls import path

from events.api import router as events_router
from ninja import NinjaAPI

api = NinjaAPI(
    urlconf="config.urls",
    title="Django Ninja Template API",
    description="基于 Django + django-ninja 的 RESTful API 后端模板",
    version="1.0.0",
)

api.add_router("/events", events_router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
