from django.db.models import Q
from account.models import User
from .models import Group
from django.shortcuts import redirect

def recent_groups(request):

    if request is None or not request.user.is_authenticated:
        return {'recent_groups': False}

    if request.user.is_authenticated:
        recent_groups = request.user.visited_groups

        
   
        return {'recent_groups': recent_groups}
    

def remove_group(request,slug):

    if request.user.is_authenticated:
        group = Group.objects.get(slug = slug)
        request.user.visited_groups.remove(group)

        
   
        return redirect(request.META.get('HTTP_REFERER', '/'))