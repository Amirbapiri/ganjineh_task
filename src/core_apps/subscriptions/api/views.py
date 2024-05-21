from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from core_apps.subscriptions.models import (
    SubscriptionPlan,
    UserSubscription,
    CreditIncreaseRequest,
)
from core_apps.profiles.models import Profile
from .serializers import (
    CreditIncreaseRequestSerializer,
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer,
    UserSubscriptionListSerializer,
)
from .permissions import IsAdminUser
from core_apps.subscriptions.signals import subscription_approved_notification


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
        serializer.save(
            user=user,
            is_approved=False,
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
        if subscription.is_approved:
            return Response(
                {"error": "This subscription has already been approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription.is_approved = True
        subscription.save()

        user = subscription.user
        user.profile.user_type = Profile.SUBSCRIBED
        user.profile.save()

        subscription_approved_notification.send(sender=self.__class__, user=user)

        serializer = self.get_serializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"], permission_classes=IsAdminUser)
    def approve_credit_increase(self, request, pk=None):
        return Response({"Approve": "TRUE"})

    @action(detail=True, methods=["patch"], permission_classes=IsAdminUser)
    def approve_monthly_limit_increase(self, request, pk=None):
        return Response({"Approve": "TRUE"})


class CreditIncreaseRequestViewSet(viewsets.ModelViewSet):
    queryset = CreditIncreaseRequest.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreditIncreaseRequestSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        increase_amount = request.data.get("increase_amount")

        if not increase_amount:
            return Response(
                {"error": "Increase amount is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            subscriptions = UserSubscription.objects.filter(
                user=user,
                is_approved=True,
            )
            if not subscriptions.exists():
                return Response(
                    {"error": "User does not have an active subscription"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            valid_subscription = None
            for subscription in subscriptions:
                if subscription.plan.credit_increase:
                    valid_subscription = subscription
                    break
            if not valid_subscription:
                return Response(
                    {
                        "error": "None of the user's subscription plans allow credit increase"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            credit_request = CreditIncreaseRequest.objects.create(
                user_subscription=valid_subscription,
                increase_amount=increase_amount,
            )
            serializer = self.get_serializer(credit_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except UserSubscription.DoesNotExist:
            return Response(
                {"error": "User does not have an active subscription"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get"], permission_classes=[IsAdminUser])
    def pending(self, request):
        pending_requests = CreditIncreaseRequest.objects.filter(is_approved=False)
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        credit_request = self.get_object()
        if credit_request.is_approved:
            return Response(
                {"error": "This request has already been approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        credit_request.is_approved = True
        credit_request.save()

        profile = credit_request.user_subscription.user.profile
        profile.allowed_daily_credits += credit_request.increase_amount
        profile.save()

        serializer = self.get_serializer(credit_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
