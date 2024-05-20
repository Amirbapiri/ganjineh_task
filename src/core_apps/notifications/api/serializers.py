from rest_framework import serializers

from core_apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient_email = serializers.ReadOnlyField(source="recipient.email")
    notification_type = serializers.CharField(source="get_notification_type_display")

    class Meta:
        model = Notification
        fields = (
            "id",
            "recipient_email",
            "title",
            "message",
            "read",
            "created_at",
            "notification_type",
        )
        read_only_fields = (
            "id",
            "recipient_email",
            "title",
            "message",
            "read",
            "created_at",
            "notification_type",
        )
