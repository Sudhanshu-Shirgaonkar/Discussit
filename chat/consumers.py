import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message,ChatRoom
from datetime import datetime

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.chatroom = self.scope['url_route']['kwargs'].get('chatroom')
        self.chat_room = ChatRoom.objects.get(id = int(self.chatroom ) )
        

   
        if not self.chatroom:
            # Handle error, chatroom parameter not provided
           return None

        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        

        self.accept()

        previous_messages = Message.objects.filter(chat_room=self.chat_room)

        # Send the previous messages to the newly connected client
        for message in previous_messages:
            time = message.timestamp.strftime('%d %b %Y %I:%M %p')
          
            self.send(text_data=json.dumps({
                'type': 'chat',
                'message': message.content,
                'sender': message.sender.username,
                'time' : str(time),
                "id": message.id
                
                
            }))


    def send_chat_message(self, event):
        message = event['message']
        sender = event['sender']
        time = event['time']

        # Do something with the message, such as logging it
        print(f"New message from {sender}: {message} at {time}")
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']
        current_time = datetime.now()
        formatted_time = current_time.strftime('%d %b %Y %I:%M %p')

        # Save the message to the database
        chat_message = Message.objects.create(
            content=message,
            sender=sender,
            chat_room=self.chat_room
        )

        # Send the message to all clients in the group except the sender
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'time': str(formatted_time),
                'exclude': self.channel_name
            }
        )

        # Send the message to the sender as well
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender.username,
            'time': str(formatted_time),
       
        }))

    def chat_message(self, event):
        # Call the send_chat_message method after sending the message to the group
        async_to_sync(self.send_chat_message(event))

        # Send the message to all clients in the group except the sender
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': event['message'],
                'sender': event['sender'].username,
                'time': str(event['time']),
                'exclude': self.channel_name
            }
        )

        # Send the message to the sender as well
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender'].username,
            'time': str(event['time'])
        }))