from django.db.models import Q
from .models import Message

def unread_message_count(request):
    if request is None or not request.user.is_authenticated:
        return {'unread_message_count': 0}

    count = Message.objects.filter(
        Q(chat_room__members=request.user) & Q(is_read=False) & ~Q(sender=request.user)
    ).count()

    return {'unread_message_count': count}
