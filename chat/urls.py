
from django.urls import path
from .import views

urlpatterns = [

    path("",views.ChatView.as_view(),name='chat'),
    path("delete_message/<int:pk>",views.delete_message,name='delete_message'),
    path("start_chat/<slug:slug>",views.create_chatroom,name='start-chat')
    

]
