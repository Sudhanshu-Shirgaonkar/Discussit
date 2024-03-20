from django.db.models import Q
from account.models import User

def group_request(request):

    if request is None or not request.user.is_authenticated:
        return {'group_notification': False}

    if request.user.is_authenticated:
        notification = request.user.group_notification.all().count()

        if notification > 0:
            notification = True
        else:
            notification = False
      
   
        return {'group_notification': notification}
