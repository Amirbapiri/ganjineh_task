from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/", include(("core_apps.api_v1", "api_v1"), namespace="api_v1")),
]
