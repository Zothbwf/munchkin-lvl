from channels.routing import URLRouter
from django.urls import path
from game import consumers

websocket_urlpatterns = [
    path("ws/game/<game_hash>/",
         consumers.GameConsumer.as_asgi(), name='ws_game_update'),
]
