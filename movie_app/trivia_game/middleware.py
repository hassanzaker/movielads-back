from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.settings import api_settings
from channels.db import database_sync_to_async
from urllib.parse import parse_qs

from users.models import CustomUser

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

@database_sync_to_async
def get_user(token):
    try:
        payload = jwt_decode_handler(token)
        user = CustomUser.objects.get(id=payload['user_id'])
        return user
    except:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that takes the token from the WebSocket URL and authenticates the user.
    """

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = scope['query_string'].decode()
        query_params = parse_qs(query_string)

        token = query_params.get('token', [None])[0]

        if token:
            scope['user'] = await get_user(token)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
