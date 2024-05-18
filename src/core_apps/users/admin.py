from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = [
        "pkid",
        "id",
        "email",
        "is_staff",
        "is_superuser",
        "is_verified",
        "is_active",
    ]
    list_display_links = ["pkid", "id", "email"]
    list_filter = [
        "email",
        "is_staff",
        "is_active",
        "is_verified",
    ]
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (
            _("Permission & Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
            ),
        },
    )
    search_fields = ["email"]
