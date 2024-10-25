"""
ASGI config for movie_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import django
django.setup()


import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from trivia_game.routing import websocket_urlpatterns
from trivia_game.middleware import JWTAuthMiddleware



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_app.settings')



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
