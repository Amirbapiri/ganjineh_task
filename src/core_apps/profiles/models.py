from datetime import date
from django.db import models
from django.contrib.auth import get_user_model

from core_apps.tokens.signals import insufficient_signal_notification

User = get_user_model()


class Profile(models.Model):
    REGULAR = "regular"
    SUBSCRIBED = "subscribed"
    ADMIN = "admin"
    USER_TYPE_CHOICES = [
        (REGULAR, "Regular"),
        (SUBSCRIBED, "Subscribed"),
        (ADMIN, "Admin"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=REGULAR,
    )
    allowed_daily_credits = models.PositiveBigIntegerField(default=10)
    spent_daily_credits = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user}'s profile"

    def reset_daily_usage(self):
        if self.user.user_subscriptions.first():
            print(self.user, self.user.user_subscriptions)
            subscription = self.user.user_subscriptions.first()
            if subscription.last_usage_date != date.today():
                self.spent_daily_credits = 0
                subscription.last_usage_date = date.today()
                subscription.save()
                self.save()

    def check_and_deduct_credits(self, token_name):
        costs = {"btc": 1, "eth": 2, "trx": 3}
        cost = costs.get(token_name.lower())
        if not cost:
            return False, "Invalid token name"

        if self.spent_daily_credits + cost > self.allowed_daily_credits:
            insufficient_signal_notification.send(
                sender=self.__class__,
                user=self.user,
            )
            return False, "Daily limit reached"

        self.spent_daily_credits += cost
        self.save()
        return True, None

    def check_and_deduct_credits_for_special_user(self, amount=10):
        if self.spent_daily_credits + amount <= self.allowed_daily_credits:
            self.spent_daily_credits += amount
            self.save()
            return True, None
        else:
            insufficient_signal_notification.send(
                sender=self.__class__,
                user=self.user,
            )
            return False, "Insufficient credits"
