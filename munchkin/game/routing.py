from django.urls import path
from game import consumers

websocket_urlpatterns = [
    path(
        "/game/<game_hash>/", consumers.GameConsumer.as_asgi(), name="ws_game_update"
    ),
]
