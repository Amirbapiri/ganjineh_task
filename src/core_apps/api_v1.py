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
    path(
        "tokens/",
        include(
            ("core_apps.tokens.api.urls", "tokens"),
            namespace="tokens",
        ),
        name="tokens",
    ),
    path(
        "notifications/",
        include(
            ("core_apps.notifications.api.urls", "notifications"),
            namespace="notifications",
        ),
        name="notifications",
    ),
]
