from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/discussion/(?P<code>\w+)/$", consumers.ChatConsumer.as_asgi()),
    # re_path(r"ws/discussion/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

# from channels.routing import route
# from .consumers import connect, message, disconnect

# channel_routing = [
#     route("websocket.connect", connect),
#     route("websocket.receive", message),
#     route("websocket.disconnect", disconnect),
# ]
