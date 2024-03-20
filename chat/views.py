from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from .models import ChatRoom,Message
from django.shortcuts import get_object_or_404,redirect,HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from urllib.parse import urlencode
from .forms import MessageForm
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from account.models import User
from django.db.models import Count
from django.db.models import Q
# Create your views here.


class ChatView(generic.ListView):
    template_name = 'chat/chat.html'
    model = ChatRoom
    context_object_name = 'chatrooms'
    form_class = MessageForm
    
    def get_queryset(self):



        
        # Get all ChatRooms for the current user
        queryset = ChatRoom.objects.filter(members=self.request.user)
        
        # Annotate the latest message for each ChatRoom
        queryset = queryset.annotate(latest_message_timestamp=Max('message__timestamp'))
        
        # Order the ChatRooms by the latest message timestamp in descending order
        queryset = queryset.order_by('-latest_message_timestamp')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add the latest message of each chat room to the context
        for chatroom in context['chatrooms']:
            latest_message = chatroom.message_set.order_by('-timestamp').first()
            chatroom.other_member = chatroom.get_other_member(self.request.user)
            if latest_message:
                chatroom.latest_message = latest_message
                
            unread_messages = chatroom.message_set.filter(
                   Q(is_read=False) & ~Q(sender=self.request.user)
                )  
            chatroom.unread = unread_messages.count()
            chatroom_id = self.request.GET.get("chatroom",None)
            chatroom = get_object_or_404(ChatRoom, id=chatroom_id) if chatroom_id else None
    
       
            if chatroom_id:
                messages = Message.objects.filter(chat_room_id=chatroom_id)
                unread_messages = Message.objects.filter(
                        Q(chat_room=chatroom) & Q(is_read=False) & ~Q(sender=self.request.user)
                    )     
                unread_messages.update(is_read = True)     
                context['messagess'] = messages
                other_user = chatroom.get_other_member(self.request.user)
                context['other_user'] = other_user

            
                



        context['findchats'] = self.request.user.following.all
        
      
                
        context['form'] = self.form_class()
        
        return context
    
 





def delete_message(request, pk):
    message= Message.objects.get(id = pk)

    message.delete()


    return redirect(request.META.get('HTTP_REFERER'))




@login_required
def create_chatroom(request,slug):
    # check if the chat room already exists

    other_user = User.objects.get(slug = slug)
    members = [request.user, other_user] # replace with the list of members
    chatroom = ChatRoom.objects.filter(members__in=members).annotate(num_members=Count('members')).filter(num_members=len(members)).first()
    if chatroom:
        # chat room already exists, redirect to it
        return redirect(reverse('chat:chat') + f'?chatroom={chatroom.id}')

    # create a new chat room
    chatroom = ChatRoom.objects.create(name=f'{request.user}+{other_user}')
    chatroom.members.set(members)

    # redirect to the new chat room
    return redirect(reverse('chat:chat') + f'?chatroom={chatroom.id}')
