from django.test import TestCase, Client
from django.urls import reverse
from chat.views import *
from users.models import User
from chat.models import ChatGroup, GroupMessage
from chat.forms import ChatmessageCreateForm


class ChatViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password2')
        self.private_chat_group = ChatGroup.objects.create(group_name='private-chat', is_private=True)
        self.private_chat_group.members.add(self.user1, self.user2)

    def test__chat_view(self):
        self.client.login(email='user1@example.com', password='password1')
        response = self.client.get(reverse('chat:chatroom', args=['private-chat']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat/chat.html')

class GetOrCreateChatroomViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user5 = User.objects.create_user(username='user5', email='user5@example.com', password='password5')
        self.user6 = User.objects.create_user(username='user6', email='user6@example.com', password='password6')
        self.chat_group = ChatGroup.objects.create(group_name='private-chat', is_private=True)
        self.chat_group.members.add(self.user5)

    def test_get_or_create_chatroom_redirect_self(self):
        self.client.login(email='user5@example.com', password='password5')
        response = self.client.get(reverse('chat:start-chat', args=['user5']))
        self.assertRedirects(response, reverse('oglasi:home'))


    def test_get_or_create_chatroom_existing_room(self):
        self.user7 = User.objects.create_user(username='user7', email='user7@example.com', password='password7')
        self.client.login(email='user7@example.com', password='password7')
        self.chat_group.members.add(self.user7)
        response = self.client.get(reverse('chat:start-chat', args=['user5']))
        self.assertRedirects(response, reverse('chat:chatroom', args=[self.chat_group.group_name]))

    def test_get_or_create_chatroom_new_room(self):
        self.client.login(email='user5@example.com', password='password5')
        self.client.login(email='user6@example.com', password='password6')
        response = self.client.get(reverse('chat:start-chat', args=['user6']))
        new_chat_group  = ChatGroup.objects.create(group_name='new-private-chat', is_private=True)
        new_chat_group .members.add(self.user5, self.user6)
        #self.assertRedirects(response, reverse('chat:chatroom', args=[new_chat_group.group_name]))
        self.assertTrue(new_chat_group.members.filter(username='user5').exists())
        self.assertTrue(new_chat_group.members.filter(username='user6').exists())