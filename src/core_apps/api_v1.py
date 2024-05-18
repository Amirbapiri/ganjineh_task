from django.urls import path, include


urlpatterns = [
    path(
        "users/",
        include(("core_apps.users.api.urls", "users"), namespace="users"),
        name="users",
    ),
]
