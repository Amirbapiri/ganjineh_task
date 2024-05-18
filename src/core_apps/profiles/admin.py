from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_type", "credits_remaining")
    search_fields = ("user__email", "user_type")
