from django.urls import path
from .consumers import *
#Autor: Stasa Zujkovic 2021/0321

websocket_urlpatterns =[
    path("ws/chatroom/<chatroom_name>", ChatroomConsumer.as_asgi()),
]