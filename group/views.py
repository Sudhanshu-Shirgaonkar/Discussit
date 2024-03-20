from typing import Any, Dict
from django import http
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.views import generic
from .models import Group
from .forms import GroupForm,EditGroupForm
from django.urls import reverse_lazy,reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from account.models import User
from django.contrib import messages
from post.models import Post,Comment
from django.db.models import Q,F
from django.db.models import Count
from django.db.models import Count, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
# Create your views here.


class GroupView(generic.DetailView):

    template_name = 'group/group.html'
    model = Group
    context_object_name = 'group'

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        user = request.user
        if user.is_authenticated:

    

            if len(user.visited_groups.all()) == 3 and group not in user.visited_groups.all() :
                user.visited_groups.remove(user.visited_groups.all()[2])
            user.visit_group(group)
        return super().get(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)
        group = self.get_object()
        posts = Post.objects.filter(
            Q(group = group) &
            Q(is_approved = True)
        )

        posts = posts.annotate(
        upvote_count=Count("upvotes"),
        downvote_count=Count("downvotes"),
        comment_count=Coalesce(
            Count("comment", distinct=True),
            Value(0),
        ) + Coalesce(
            Count(
                Case(
                    When(comment__reply__isnull=False, then=1),
                    output_field=IntegerField(),
                    distinct=True,
                            )
                        ),
                        Value(0),
                    ),
                )
        if (
            self.request.GET.get("feed") == None
            and self.request.GET.get("sortby") == None
            and self.request.GET.get("category") == None
        ):
            
            posts = posts.annotate(
                combine =  Count("upvotes",distinct=True)  + F('comment_count'),
             
            ).order_by("-combine")

        if (self.request.GET.get("sortby") == 'new'):

            posts = posts.order_by("-created_at")


        related_groups = Group.objects.filter(
            Q(category = group.category) &
            ~Q(id = group.id)
            )
        context['related_groups'] = related_groups[:5]
        context['posts'] = posts
        context['approve_posts'] = Post.objects.filter(group = group,is_approved = False).count()
 
        return context


@login_required
def group_join(request, slug):
    group = get_object_or_404(Group, slug=slug)

    if group.approve_members == True:
        messages.info(request,f'Request send for approval in {group}')
        group.approval.add(request.user)
      
    else:
        group.member.add(request.user)
        messages.info(request,f'Successfully Joined group "{group}" ')
    

    group.save()

    if group.group_type == 'Private' and request.user not in group.member.all():
   
        return redirect('index:private-group', slug=slug)
    
    else:
     
        return redirect('group:group', slug=slug)

@login_required
def group_leave(request, slug):
    group = get_object_or_404(Group, slug=slug)

    if request.user in group.member.all():
        group.member.remove(request.user)
        messages.info(request,f'Successfully Left group "{group}" ')

    if request.user in group.approval.all():
        group.approval.remove(request.user)
        messages.info(request,'Canceled request to join group')


    group.save()

    if group.group_type == 'Private' and request.user not in group.member.all():

        return redirect('index:private-group', slug=slug)
    
    else:
       
        return redirect('group:group', slug=slug)




class CreateGroupView(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):

    template_name = 'group/create_group.html'
    model = Group
    form_class = GroupForm
    success_message = "Group Created Successfully!!"

    def form_valid(self, form):
        group = form.save(commit=False)
        group.save()  # Save the group object first
        group.admins.add(self.request.user)
        group.member.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group:group', kwargs={'slug': self.object.slug})
    

class EditGroupView(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView):

    template_name = 'group/group_settings.html'
    model =Group
    form_class = EditGroupForm
    context_object_name = 'group'
    success_message = "Group Updated"

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
    


class AdminModView(LoginRequiredMixin, generic.DetailView):
    model = Group
    template_name = 'group/manage_admin_mod.html'
    context_object_name  ='group'

    def get_success_url(self):
        return reverse_lazy('group:admin_mod', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        group = self.object

        # Add the list of moderators and admins to the context
        context['moderators'] = group.moderator.all()
        context['admins'] = group.admins.all()


        context['moderators_request'] = group.moderator_request.all()
        context['admins_request'] = group.admins_request.all()

        return context

    def post(self, request, *args, **kwargs):
        group = self.get_object()

        # Check if the request is for adding a new admin/moderator or updating an existing one
        if 'action' in request.POST:
            user_id = request.POST.get('user')
            select = request.POST.get('select')
            user = User.objects.get(id=user_id)


            if select == 'remove':

                if user in group.moderator.all():
                   
                    group.moderator.remove(user)

                if user in group.admins.all():
                  
                    group.admins.remove(user)

            if select == 'makeadmin':

                if user in group.moderator.all():
                
                    group.moderator.remove(user)
                    group.admins.add(user)


            if select == 'makemod':

                if user in group.admins.all():
                
                    group.admins.remove(user)
                    group.moderator.add(user)



        if 'add' in request.POST:
            user = request.POST.get('user')
            role = request.POST.get('role')
            try:
                user = User.objects.get(username=user)

            except User.DoesNotExist:
                messages.error(request, "This user does not exist.")
                return redirect('group:admin_mod', slug=group.slug)



         
            if role == 'moderator':
                if user in  group.moderator.all():
                    messages.error(request, "This user is already moderator")
                    return redirect('group:admin_mod', slug=group.slug)
                
                if user in  group.moderator_request.all():
                    messages.error(request, "You already sent this user request for moderator")
                    return redirect('group:admin_mod', slug=group.slug)
                
                if user in  group.admins.all():
                    messages.error(request, "This user is already admin")
                    return redirect('group:admin_mod', slug=group.slug)
                

                if user in  group.admins_request.all():
                    messages.error(request, "You already sent this user request for Admin")
                    return redirect('group:admin_mod', slug=group.slug)
                

                if user in  group.member.all():
                    group.moderator_request.add(user)
                    user.group_notification.add(group)

                else:
                    messages.error(request, "This user should be member before assigning them role")
                    return redirect('group:admin_mod', slug=group.slug)



            if role == 'admin':
                if user in  group.moderator.all():
                    messages.error(request, "This user is already moderator")
                    return redirect('group:admin_mod', slug=group.slug)
                
                if user in  group.moderator_request.all():
                    messages.error(request, "You already sent this user request for moderator")
                    return redirect('group:admin_mod', slug=group.slug)
                
                if user in  group.admins.all():
                    messages.error(request, "This user is already admin")
                    return redirect('group:admin_mod', slug=group.slug)
                

                if user in  group.admins_request.all():
                    messages.error(request, "You already sent this user request for Admin")
                    return redirect('group:admin_mod', slug=group.slug)
                

                if user in  group.member.all():
                    group.admins_request.add(user)
                    user.group_notification.add(group)

                else:
                    messages.error(request, "This user should be member before assigning them role")
                    return redirect('group:admin_mod', slug=group.slug)
  

        if 'cancel' in request.POST:
            user_id = request.POST.get('user')

            user = User.objects.get(id=user_id)

            if user in group.admins_request.all():
                group.admins_request.remove(user)
                messages.success(request, f"Request for making {user} admin is cancelled")

            if user in group.moderator_request.all():
                group.moderator_request.remove(user)
                messages.success(request, f"Request for making {user} moderator  is cancelled")

            if group in user.group_notification.all():

                user.group_notification.remove(group)



   
           


        return redirect('group:admin_mod', slug=group.slug)
    
    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
       

        if self.request.user not  in group.admins.all() or self.request.user not  in group.member.all():
            return redirect(request.META.get('HTTP_REFERER', '/'))


        return super().dispatch(request, *args, **kwargs)
    




class ApproveMemberView(LoginRequiredMixin, generic.DetailView):
    model = Group
    template_name = 'group/approve_user.html'
    context_object_name  ='group'

    def get_success_url(self):
        return reverse_lazy('group:approve-user', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        group = self.object

        # Add the list of moderators and admins to the context
        context['approvals'] = group.approval.all()
  

        return context


    def post(self, request, *args, **kwargs):
        group = self.get_object()

        # Check if the request is for adding a new admin/moderator or updating an existing one
        if 'approve' in request.POST:
            user_id = request.POST.get('user')
            select = request.POST.get('select')
            user = User.objects.get(id=user_id)

            if select == 'remove':

                if user in group.approval.all():
              
                    group.approval.remove(user)

            if select == 'approve':

        
          
                if user in group.approval.all():
              
                    group.approval.remove(user)
                    group.member.add(user)


        return redirect('group:approve-user', slug=group.slug)
    
    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
       

        if self.request.user not  in group.admins.all() or self.request.user not  in group.member.all():
            return redirect(request.META.get('HTTP_REFERER', '/'))


        return super().dispatch(request, *args, **kwargs)

class BlockedUsersView(LoginRequiredMixin, generic.DetailView):
    model = Group
    template_name = 'group/block_remove_user.html'
    context_object_name  ='group'

    def get_success_url(self):
        return reverse_lazy('group:block-remove', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        group = self.object

        # Add the list of moderators and admins to the context
        context['blocked'] = group.blocked.all()
       

        return context

    def post(self, request, *args, **kwargs):
        group = self.get_object()

        # Check if the request is for adding a new admin/moderator or updating an existing one
        if 'handleblock' in request.POST:
            user_id = request.POST.get('user')
            select = request.POST.get('select')
            user = User.objects.get(id=user_id)
 
            if select == 'unblock':

                if user in group.blocked.all():
         
                    group.blocked.remove(user)




        if 'block' in request.POST:
            user = request.POST.get('user')
            choice = request.POST.get('choice')
            try:
                user = User.objects.get(username=user)

            except User.DoesNotExist:
                messages.error(request, "This user does not exist.")
                return redirect('group:block-remove', slug=group.slug)



         
            if choice == 'remove':
                if user in  group.moderator.all():

                    group.moderator.remove(user)

                
                if user in  group.admins.all():
                    group.admins.remove(user)
                
                if user in  group.member.all():
                    group.member.remove(user)

                else:
                    messages.error(request, "This user does not belong to this group")
                    return redirect('group:block-remove', slug=group.slug)
                
                messages.error(request, f"{user} was removed")



            if choice == 'block':
                group.blocked.add(user)
                if user in  group.moderator.all():

                    group.moderator.remove(user)

                
                if user in  group.admins.all():
                    group.admins.remove(user)
                
                if user in  group.member.all():
                    group.member.remove(user)

                else:
                    messages.error(request, f"{user}")
                    return redirect('group:block-remove', slug=group.slug)
                
                messages.error(request, f"{user} was Blocked")
  

        return redirect('group:block-remove', slug=group.slug)
    

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
       

        if self.request.user not  in group.admins.all() or self.request.user not  in group.member.all():
            return redirect(request.META.get('HTTP_REFERER', '/'))


        return super().dispatch(request, *args, **kwargs)



class ApprovePostView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'group/approve_post.html'
    context_object_name  ='posts'

    def get_success_url(self):
        return reverse_lazy('group:approve-post', kwargs={'slug': self.object.slug})
    
    def get_queryset(self):
        group = self.get_object()
        querySet = Post.objects.filter(
            Q(group= group) &
            Q(is_approved= False) 
           
        )
        return querySet

    def get_object(self, queryset=None):
        group_slug = self.kwargs.get('slug')
        group = get_object_or_404(Group, slug=group_slug)
        return group

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        group = self.get_object()

        # Add the list of moderators and admins to the context
        context['group'] = group
       

        return context

    def post(self, request, *args, **kwargs):
        group = self.get_object()

  
        if 'approve' in request.POST:
            post_id = request.POST.get('post')
            select = request.POST.get('select')
            post = Post.objects.get(id=post_id)
 
            if select == 'approve':

                post.is_approved = True
                post.save()

            if select == 'remove':

             
                post.delete()                 

        return redirect('group:approve-post', slug=group.slug)
    
    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
       

        if self.request.user not  in group.admins.all() or self.request.user not  in group.member.all():
            return redirect(request.META.get('HTTP_REFERER', '/'))


        return super().dispatch(request, *args, **kwargs)   

class DeleteGroupView(LoginRequiredMixin,generic.DeleteView):

    model = Group

    def get_success_url(self):
 
    
        return reverse_lazy('index:index')

    

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, f"Group Deleted Successfully")
        return HttpResponseRedirect(self.get_success_url())
    


class BlockedMemberMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and is trying to access a group page
        if request.user.is_authenticated and request.path.startswith('/g/'):

            # Get the group ID from the URL
            slug = request.path.split('/')[2]

            # Check if the group exists and if the user is blocked from it
            try:
                group = Group.objects.get(slug=slug)
            except ObjectDoesNotExist:
                # Return the response and let the middleware continue to the next middleware in the chain or the view function.
                return self.get_response(request)

            if request.user in group.blocked.all():
                # Redirect the user to a different page
       
                return redirect(reverse('index:blocked-group', kwargs={'slug': group.slug}))
          

        response = self.get_response(request)
        return response
    


class PrivateGroupMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and is trying to access a group page
        if  request.path.startswith('/g/'):

            # Get the group ID from the URL
            slug = request.path.split('/')[2]

            # Check if the group exists and if the user is blocked from it
            try:
                group = Group.objects.get(slug=slug)

            except ObjectDoesNotExist:
                # Return the response and let the middleware continue to the next middleware in the chain or the view function.
                return self.get_response(request)

            if group.group_type == 'Private' and request.user not in group.member.all() :
                # Redirect the user to a different page
                print("sfffffffffffffffffffffff")
                return redirect(reverse('index:private-group', kwargs={'slug': group.slug}))
            

            


            


          

        response = self.get_response(request)
        return response

