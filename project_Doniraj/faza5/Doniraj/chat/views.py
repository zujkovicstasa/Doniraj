from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from django.http import Http404
from users.models import User 
from .models import *
from .forms import *
#Autor: Stasa Zujkovic 2021/0321
@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    
    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
            
    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()

            context = {
                'message' : message,
                'user' : request.user
            }
            return render(request, 'chat/partials/chat_message_p.html', context)
    
    context = {
        'chat_messages' : chat_messages, 
        'form' : form,
        'other_user' : other_user,
        'chatroom_name' : chatroom_name,
    }
    
    return render(request, 'chat/chat.html', context)

@login_required
def get_or_create_chatroom(request, username):
    
    if request.user.username == username:
        return redirect('oglasi:home')
    
    try: 
        other_user = User.objects.get(username = username)
    except User.DoesNotExist:

        raise Http404("User does not exist")
    print(other_user.username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    roomexists = False;
    if my_chatrooms.exists():
        for room in my_chatrooms:
            if other_user in room.members.all():
                chatroom = room
                roomexists= True;
                break
            
        if not roomexists:
            chatroom = ChatGroup.objects.create(is_private = True)
            chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private = True)
        chatroom.members.add(other_user, request.user)
    print(chatroom.members)
    return redirect('chat:chatroom', chatroom.group_name)

