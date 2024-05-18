from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    daily_credits = models.PositiveIntegerField()
    token_access = models.BooleanField(default=False)
    credit_increase = models.BooleanField(default=False)

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
    credits_remaining = models.PositiveIntegerField()
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.plan.name}"
