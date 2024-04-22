from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/discussion/(?P<code>\w+)/$", consumers.ChatConsumer.as_asgi()),
    # re_path(r"ws/discussion/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]