from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    token_access = models.BooleanField(default=False)
    credit_increase = models.BooleanField(default=False)
    monthly_credit_increase = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name="user_subscriptions",
    )
    is_approved = models.BooleanField(default=True)
    last_usage_date = models.DateField(null=True, blank=True)
    monthly_limit_increase = models.BooleanField(default=False)
    monthly_limit_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.plan.name}"


class CreditIncreaseRequest(models.Model):
    user_subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.CASCADE,
        related_name="credit_increase_requests",
    )
    increase_amount = models.PositiveIntegerField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Credit Increase Request for {self.user_subscription.user} - {self.increase_amount} credits"


class MonthlyLimitIncreaseRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="monthly_limit_increase_requests",
    )
    requested_credits = models.PositiveIntegerField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Monthly Limit Increase Request for {self.user} - {self.requested_credits} credits"
