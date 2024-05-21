from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.authentication import JWTAuthentication

import logging

logger = logging.getLogger(__name__)


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        if token:
            token = token[0]  # Assuming it's the first token in the query string
            user = await self.get_user_from_token(token)
            scope["user"] = user if user else AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            return jwt_auth.get_user(validated_token)
        except Exception as e:
            logger.error(f"JWT Authentication failed: {str(e)}")
            return None
