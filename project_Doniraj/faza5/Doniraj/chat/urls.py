from django.urls import path
from .views import *
#Autor: Stasa Zujkovic 2021/0321
app_name = 'chat'

urlpatterns = [
    path('', chat_view, name="home"),
    path('chat/<username>', get_or_create_chatroom, name="start-chat"),
    path('chatroom/<chatroom_name>', chat_view, name="chatroom"),
    
]