from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import RegisterAPIView


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path(
        "jwt/",
        include(
            (
                [
                    path("login/", TokenObtainPairView.as_view(), name="jwt_login"),
                    path("refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
                    path("verify/", TokenVerifyView.as_view(), name="jwt_verify"),
                ]
            )
        ),
        name="jwt",
    ),
]
