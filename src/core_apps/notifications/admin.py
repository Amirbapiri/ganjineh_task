from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "title", "message", "read", "created_at")
    list_filter = ("read", "created_at")
    search_fields = ("title", "message", "recipient__username")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
