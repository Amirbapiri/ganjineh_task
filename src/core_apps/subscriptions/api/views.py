from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core_apps.subscriptions.models import SubscriptionPlan, UserSubscription
from core_apps.profiles.models import Profile
from .serializers import (
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer,
    UserSubscriptionListSerializer,
)
from .permissions import IsAdminUser


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


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "pk"

    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def pending(self, request, pk=None):
        pending_subscriptions = UserSubscription.objects.filter(is_approved=False)
        serializer = self.get_serializer(pending_subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        subscription = self.get_object()
        subscription.is_approved = True
        subscription.credits_remaining = subscription.plan.daily_credits
        subscription.save()

        # TODO could be done via signals
        # Update user_type after subscription approval
        user = subscription.user
        user.profile.user_type = Profile.SUBSCRIBED
        user.profile.save()

        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)
