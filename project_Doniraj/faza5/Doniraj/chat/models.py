from django.db import models
from users.models import User
from django.conf import settings
import shortuuid
#Autor: Stasa Zujkovic 2021/0321
class ChatGroup(models.Model):
    group_name=models.CharField(max_length=128,unique=True, default = shortuuid.uuid)
    members = models.ManyToManyField(User,related_name='chat_groups',blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name
    
class GroupMessage(models.Model):
    group=models.ForeignKey(ChatGroup,related_name='chat_messages', on_delete=models.CASCADE)
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
class Meta:
    orderig =['-created']
    