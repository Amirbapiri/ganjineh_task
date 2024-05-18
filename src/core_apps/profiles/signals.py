import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            user_type = Profile.ADMIN
        else:
            user_type = Profile.REGULAR

        Profile.objects.create(user=instance, user_type=user_type)
        logger.info(f"{instance}'s profile has been created.")
    else:
        instance.profile.save()
        logger.info(f"{instance}'s profile has been updated.")
