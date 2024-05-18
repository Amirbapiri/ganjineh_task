from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SubscriptionPlanListView,
    UserSubscriptionCreateView,
    UserSubscriptionViewSet,
)


router = DefaultRouter()
router.register(r"", UserSubscriptionViewSet, basename="subscription")

urlpatterns = [
    path(
        "plans/",
        SubscriptionPlanListView.as_view(),
        name="plans_list",
    ),
    path(
        "subscribe/",
        UserSubscriptionCreateView.as_view(),
        name="user-subscribe",
    ),
    path("", include(router.urls)),
]
