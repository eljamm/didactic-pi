import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class ReadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sensor_name = self.scope['url_route']['kwargs']['sensor_name']
        self.sensor_group_name = 'sensor_%s' % self.sensor_name

        # Join sensor group
        await self.channel_layer.group_add(
            self.sensor_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave sensor group
        await self.channel_layer.group_discard(
            self.sensor_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to group
        await self.channel_layer.group_send(
            self.sensor_group_name,
            {
                'type': 'sensor_message',
                'message': message
            }
        )

    # Receive message from group
    async def sensor_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
