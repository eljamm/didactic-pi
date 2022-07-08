from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sensor/read/(?P<sensor_name>\w+)/$',
            consumers.ReadConsumer.as_asgi()),
]
