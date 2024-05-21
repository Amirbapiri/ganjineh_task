from rest_framework import serializers

from core_apps.subscriptions.models import (
    SubscriptionPlan,
    UserSubscription,
    CreditIncreaseRequest,
    MonthlyLimitIncreaseRequest,
)


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=SubscriptionPlan.objects.all())

    class Meta:
        model = UserSubscription
        fields = ("plan",)


class UserSubscriptionListSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserSubscription
        fields = (
            "id",
            "user",
            "plan",
            "is_approved",
            "monthly_limit_increase",
            "monthly_limit_expiry",
        )


class CreditIncreaseRequestSerializer(serializers.ModelSerializer):
    user_subscription = serializers.PrimaryKeyRelatedField(
        queryset=UserSubscription.objects.all()
    )

    class Meta:
        model = CreditIncreaseRequest
        fields = (
            "id",
            "user_subscription",
            "increase_amount",
            "is_approved",
            "created_at",
            "approved_at",
        )


class MonthlyLimitIncreaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyLimitIncreaseRequest
        fields = ("id", "user", "requested_credits", "is_approved", "approved_at")
        extra_kwargs = {"user": {"read_only": True}}
