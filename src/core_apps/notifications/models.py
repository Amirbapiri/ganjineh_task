from django.db import models
from django.contrib.auth import get_user_model

from core_apps.common.models import TimestampModel


User = get_user_model()


class Notification(TimestampModel):
    NOTIFICATION_TYPES = (
        ("ALERT", "Alert"),
        ("MSG", "Message"),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    updated_at = None

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.recipient.email}"
