from core_apps.notifications.models import Notification


def create_notification(user, title, message, notification_type="MSG"):
    Notification.objects.create(
        recipient=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )
