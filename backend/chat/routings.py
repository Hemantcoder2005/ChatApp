# chat/routing.py
from django.urls import re_path

from . import consumers
# from notification import consumer as NotificationConsumer
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    #re_path(r"ws/notification/(?P<room_name>\w+)/$", NotificationConsumer.Consumer.as_asgi()),
]