from django.db import models
from django.contrib.auth import get_user_model
from datetime import date


User = get_user_model()


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    daily_credits = models.PositiveIntegerField()
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
    daily_usage = models.PositiveBigIntegerField(default=0)
    last_usage_date = models.DateField(null=True, blank=True)
    monthly_limit_increase = models.BooleanField(default=False)
    monthly_limit_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.plan.name}"

    def reset_daily_usage(self):
        if self.last_usage_date != date.today():
            self.daily_usage = 0
            self.last_usage_date = date.today()
            self.save()


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
