from django.dispatch import receiver

from core_apps.tokens.signals import insufficient_signal_notification
from core_apps.subscriptions.signals import subscription_approved_notification
from .models import Notification


@receiver(insufficient_signal_notification)
def create_insufficient_notification(sender, **kwargs):
    user = kwargs.get("user")
    notification = Notification.objects.create(
        recipient=user,
        title="Insufficient credits",
        message="Your credits have run out.",
        notification_type="ALERT",
    )


@receiver(subscription_approved_notification)
def create_subscription_approved_notification(sender, **kwargs):
    user = kwargs.get("user")
    notification = Notification.objects.create(
        recipient=user,
        title="Subscription approved",
        message="Your subscription has been approved.",
        notification_type="ALERT",
    )
