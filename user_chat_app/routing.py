from django.urls import re_path

from .consumers import UserChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/v1/chat/$", UserChatConsumer.as_asgi()),
]
