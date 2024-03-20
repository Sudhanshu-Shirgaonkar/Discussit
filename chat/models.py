from django.db import models
from account.models import User

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    

    def __str__(self):
        return self.name
    
    def get_other_member(self, user):
        return self.members.exclude(id=user.id).first() if self.members.count() > 1 else None
    

   

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} said '{self.content}' in {self.chat_room} at {self.timestamp}"