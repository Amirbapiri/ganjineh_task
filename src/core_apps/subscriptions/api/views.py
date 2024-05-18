from rest_framework import generics, permissions

from core_apps.subscriptions.models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer


class SubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = (permissions.AllowAny,)


class UserSubscriptionCreateView(generics.CreateAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        plan = serializer.validated_data.get("plan")
        daily_credits = plan.daily_credits
        serializer.save(
            user=user,
            is_approved=False,
            credits_remaining=daily_credits,
        )

