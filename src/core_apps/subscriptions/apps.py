from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriptionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.subscriptions"
    verbose_name = _("Subscriptions")
    verbose_name_plural = _("Subscriptions")
