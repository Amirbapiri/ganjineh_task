from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    REGULAR = "regular"
    SUBSCRIBED = "subscribed"
    USER_TYPE_CHOICES = [
        (REGULAR, "Regular"),
        (SUBSCRIBED, "Subscribed"),
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
    credits_remaining = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.user}'s profile"
