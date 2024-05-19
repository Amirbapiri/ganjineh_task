from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TokensConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.tokens"
    verbose_name = _("Token")
    verbose_name_plural = _("Tokens")
