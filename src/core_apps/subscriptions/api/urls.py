from django.urls import path

from .views import SubscriptionPlanListView, UserSubscriptionCreateView

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
]
