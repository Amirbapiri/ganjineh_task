from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SubscriptionPlanListView,
    UserSubscriptionCreateView,
    UserSubscriptionViewSet,
    CreditIncreaseRequestViewSet,
)


router = DefaultRouter()
router.register(
    r"user-subscriptions",
    UserSubscriptionViewSet,
    basename="user-subscription",
)
router.register(
    r"credit-requests",
    CreditIncreaseRequestViewSet,
    basename="credit-request",
)

urlpatterns = [
    path("plans/", SubscriptionPlanListView.as_view(), name="plans_list"),
    path("subscribe/", UserSubscriptionCreateView.as_view(), name="user-subscribe"),
    path("", include(router.urls)),
]
