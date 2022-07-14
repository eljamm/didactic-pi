import json
import logging

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import (AsyncWebsocketConsumer,
                                        WebsocketConsumer)
from django.utils import timezone
from .models import Sensor, Raspi


class PiConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pi_name = self.scope['url_route']['kwargs']['pi_name']
        self.pi_group_name = 'pi_%s' % self.pi_name

        # Join Pi group
        await self.channel_layer.group_add(
            self.pi_group_name,
            self.channel_name
        )

        await self.accept()

    def get_name(self, name):
        return Raspi.objects.get(name=name).name

    async def disconnect(self, close_code):
        # Leave Pi group
        await self.channel_layer.group_discard(
            self.pi_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        # Send message to group
        await self.channel_layer.group_send(
            self.pi_group_name,
            {
                'type': 'sensor_message',
                'message': message,
                'time': now.isoformat()
            }
        )

    # Receive message from group
    async def sensor_message(self, event):
        message = event['message']
        now = event['time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'time': now
        }))
