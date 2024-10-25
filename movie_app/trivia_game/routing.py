from django.urls import path
from .consumers import GameRoomConsumer

websocket_urlpatterns = [
    path('ws/game/', GameRoomConsumer.as_asgi()),
]
