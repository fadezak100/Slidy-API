import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CommentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'owner'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_comment',
                'message': comment
            }
        )

    async def broadcast_comment(self, event):
        comment = event['message']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': comment
        }))


chat_consumer = CommentsConsumer.as_asgi()
