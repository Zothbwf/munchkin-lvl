import json

from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_hash = self.scope["url_route"]["kwargs"]["game_hash"]
        self.room_group_name = f"{self.game_hash}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def game_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "game.update",
                }
            )
        )

    async def game_delete(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "game.delete",
                }
            )
        )
