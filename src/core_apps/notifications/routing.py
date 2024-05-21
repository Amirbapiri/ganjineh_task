from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from core_apps.notifications.consumers import NotificationConsumer


websocket_urlpatterns = [
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]
