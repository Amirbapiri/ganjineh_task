from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.notifications"
    verbose_name = _("Notification")
    verbose_name_plural = _("Notifications")

    def ready(self):
        import core_apps.notifications.receivers

        return super().ready()
