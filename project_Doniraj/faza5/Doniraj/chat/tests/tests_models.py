from django.test import TestCase
from django.utils import timezone
from chat.models import ChatGroup, GroupMessage
from users.models import User
import shortuuid


class ChatGroupModelTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password2')
        self.chat_group = ChatGroup.objects.create(group_name='Test Group')

    def test_chat_group_creation(self):
        self.assertEqual(self.chat_group.group_name, 'Test Group')
        self.assertFalse(self.chat_group.is_private)
        self.assertEqual(self.chat_group.members.count(), 0)

    def test_add_members_to_chat_group(self):
        self.chat_group.members.add(self.user1, self.user2)
        self.assertEqual(self.chat_group.members.count(), 2)
        self.assertIn(self.user1, self.chat_group.members.all())
        self.assertIn(self.user2, self.chat_group.members.all())

    def test_chat_group_str_method(self):
        self.assertEqual(str(self.chat_group), 'Test Group')


class GroupMessageModelTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password2')
        self.chat_group = ChatGroup.objects.create(group_name='Test Group')
        self.group_message = GroupMessage.objects.create(
            group=self.chat_group,
            author=self.user1,
            body='Test Message',
            created=timezone.now()
        )

    def test_group_message_creation(self):
        self.assertEqual(self.group_message.group, self.chat_group)
        self.assertEqual(self.group_message.author, self.user1)
        self.assertEqual(self.group_message.body, 'Test Message')

    def test_group_message_str_method(self):
        self.assertEqual(str(self.group_message), f'{self.user1.username} : Test Message')

    def test_group_message_ordering(self):
        
        GroupMessage.objects.create(
            group=self.chat_group,
            author=self.user1,
            body='Test Message 2',
            created=timezone.now()
        )
        messages = GroupMessage.objects.all()
        self.assertEqual(messages[1].body, 'Test Message 2')
        self.assertEqual(messages[0].body, 'Test Message')
