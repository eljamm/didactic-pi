from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<pi_name>\w+)/$',
            consumers.PiConsumer.as_asgi()),
    re_path(r'ws/(?P<pi_name>\w+)/(?P<sensor_name>\w+)/$',
            consumers.PiConsumer.as_asgi()),
]