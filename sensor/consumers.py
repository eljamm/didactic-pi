import json
import logging

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import (AsyncWebsocketConsumer,
                                        WebsocketConsumer)
from django.utils import timezone
from .models import Sensor, Raspi, Item


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
        
        sensor = ''
        dht11_json = ''
        now = timezone.now()

        try:
            sensor = text_data_json['sensor']
        except Exception as e:
            logging.debug(e.args[0])
        finally:
            generic_json = {
            'type': 'sensor_message',
            'sensor': sensor,
            'message': message,
            'time': now.isoformat()
        }

        if (sensor == 'dht11'):
            temp = text_data_json['temp']
            hum = text_data_json['hum']

            dht11_json = {
                'temp': temp,
                'hum': hum,
            }

            json_file = {**generic_json, **dht11_json}

        else:
            json_file = generic_json

        # Send message to group
        await self.channel_layer.group_send(
            self.pi_group_name, json_file
        )

    # Receive message from group
    async def sensor_message(self, event):
        message = event['message']
        sensor = event['sensor']
        now = event['time']

        # Write message to database
        await self.register_data(self.pi_name, sensor, now, message)

        generic_json = {
            'sensor': sensor,
            'message': message,
            'time': now
        }

        if (sensor == 'dht11'):
            temp = event['temp']
            hum = event['hum']

            dht11_json = {
                'temp': temp,
                'hum': hum,
            }

            json_file = {**generic_json, **dht11_json}

        else:
            json_file = generic_json

        # Send message to WebSocket
        await self.send(text_data=json.dumps(json_file))

    @database_sync_to_async
    def register_data(self, raspi, sensor, time, data):
        try:
            pi = Raspi.objects.get(name=raspi)
            se = pi.sensor_set.get(name=sensor)
            se.item_set.create(datetime=time, data=data)
        except:
            #logging.debug("Raspi: %s | Sensor: %s | Time: %s | Data: %s" % (raspi, sensor, time, data))
            logging.debug("Sensor does not exist in database")
