"""
ASGI config for ganjineh_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ganjineh_api.settings")

django_asgi_app = get_asgi_application()

from core_apps.notifications import routing
from core_apps.notifications.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddleware(
            AuthMiddlewareStack(
                URLRouter(routing.websocket_urlpatterns),
            ),
        ),
    }
)
