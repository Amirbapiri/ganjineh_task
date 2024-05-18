from django.urls import path, include


urlpatterns = [
    path(
        "users/",
        include(("core_apps.users.api.urls", "users"), namespace="users"),
        name="users",
    ),
    path(
        "subscriptions/",
        include(
            ("core_apps.subscriptions.api.urls", "subscriptions"),
            namespace="subscriptions",
        ),
        name="subscriptions",
    ),
]
