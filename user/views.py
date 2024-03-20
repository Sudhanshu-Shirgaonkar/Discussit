from typing import Any, Dict
from django.shortcuts import render,redirect
from django.views import generic
from account.models import User
from post.models import Post,Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q,F
from group.models import Group
from django.db.models import Count, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


class UserView(generic.DetailView):

    template_name = 'user/profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)
        user = self.get_object()
        posts = Post.objects.filter(author=user)

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
        # Add the list of moderators and admins to the context
        if self.request.user.is_authenticated:
            context['submitted_posts'] = Post.objects.filter(author = self.request.user,is_approved = False).count()
            print(Post.objects.filter(author = self.request.user,is_approved = False).count())
       
        if (
            self.request.GET.get("feed") == None
            and self.request.GET.get("sortby") == None
            and self.request.GET.get("category") == None
        ):
            print("here")
            posts = posts.annotate(
                combine =  Count("upvotes",distinct=True)  + F('comment_count'),
             
            ).order_by("-combine")

        if (self.request.GET.get("sortby") == 'new'):

            posts = posts.order_by("-created_at")

        context['posts'] = posts
        return context
    




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
         
                 
  

        return redirect('group:approve-post', slug=group.slug)

@login_required
def follow(request, slug):
    user = get_object_or_404(User, slug=slug)
    me = User.objects.get(id = request.user.id)


    if request.user in user.followers.all():
        user.followers.remove(request.user)
        me.following.remove(request.user)


    else:

        user.followers.add(request.user)
        me.following.add(user)
        user.new_follower = True

    user.save()
    return redirect('user:user', slug=slug)






class SubmittedPostView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'user/submitted_post.html'
    context_object_name  ='posts'

    def get_success_url(self):
        return reverse_lazy('user:submitted-post', kwargs={'slug': self.object.slug})
    
    def get_queryset(self):

        querySet = Post.objects.filter(
            Q(author= self.request.user) &
            Q(is_approved= False) 
           
        )
        return querySet

    def get_object(self, queryset=None):
        user_slug = self.kwargs.get('slug')
        group = get_object_or_404(User, slug=user_slug)
        return group

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     group = self.object

    #     # Add the list of moderators and admins to the context
    #     context['blocked'] = group.blocked.all()
       

    #     return context

    def post(self, request, *args, **kwargs):
        group = self.get_object()

  
        if 'approve' in request.POST:
            post_id = request.POST.get('post')
            select = request.POST.get('select')
            post = Post.objects.get(id=post_id)
 
            if select == 'approve':

                post.is_approved = True
                post.save()
         
                 
  

        return redirect('group:approve-post', slug=group.slug)
    




class MyGroupView(generic.ListView):

    model = Group
    template_name = 'user/my_groups.html'
    context_object_name  ='groups'

    def get_success_url(self):
        return reverse_lazy('user:my-groups', kwargs={'slug': self.object.slug})
    
    def get_queryset(self):

        querySet = Group.objects.filter(
            Q(admins = self.request.user) |
            Q(moderator = self.request.user) 
           
        )
        return querySet

    def get_object(self, queryset=None):
        user_slug = self.kwargs.get('slug')
        group = get_object_or_404(User, slug=user_slug)
        return group

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        self.request.user.group_notification.clear()
      
        
        # Add the list of moderators and admins to the context
        context['group_requests'] = Group.objects.filter(
            Q(admins_request = self.request.user)|
            Q(moderator_request = self.request.user)
        )
  
       

        return context

    def post(self, request, *args, **kwargs):
        group = self.get_object()

        if 'accept' in request.POST:
            group_id = request.POST.get('group')
            group = Group.objects.get(id = group_id)
          
            if self.request.user in group.admins_request.all():

                group.admins.add(self.request.user)
                group.admins_request.remove(self.request.user)


            if self.request.user in group.moderator_request.all():

                group.moderator.add(self.request.user)
                group.moderator_request.remove(self.request.user)


        if 'cancel' in request.POST:
            group_id = request.POST.get('group')
            group = Group.objects.get(id = group_id)
          
            if self.request.user in group.admins_request.all():

                group.admins_request.remove(self.request.user)


            if self.request.user in group.moderator_request.all():

                group.moderator_request.remove(self.request.user)


        return redirect('user:my-groups', slug=self.request.user.slug)
    







class FollowingView(generic.ListView):

    model = User
    template_name = 'user/following.html'
    context_object_name  ='following'

    def get_success_url(self):
        return reverse_lazy('user:following', kwargs={'slug': self.object.slug})
    
    def get_queryset(self):

        querySet = self.request.user.following.all()

        return querySet

    def get_object(self, queryset=None):
        user_slug = self.kwargs.get('slug')
        group = get_object_or_404(User, slug=user_slug)
        return group



    def post(self, request, *args, **kwargs):
        my_user = self.get_object()

        if 'unfollow' in request.POST:
            user_id = request.POST.get('user')
            user = User.objects.get(id = user_id)
          
            if user in my_user.following.all():

             
                my_user.following.remove(user)

            if my_user in user.followers.all():
                 user.followers.remove(my_user)
               



        return redirect('user:following', slug=self.request.user.slug)
    





class FollowerView(generic.ListView):

    model = User
    template_name = 'user/followers.html'
    context_object_name  ='followers'

    def get_success_url(self):
        return reverse_lazy('user:followers', kwargs={'slug': self.object.slug})
    
    def get_queryset(self):
        
        querySet = self.request.user.followers.all()

        return querySet
    
    def get(self, request, *args, **kwargs):
        self.request.user.new_follower = False
        self.request.user.save()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        user_slug = self.kwargs.get('slug')
        group = get_object_or_404(User, slug=user_slug)
        return group



    def post(self, request, *args, **kwargs):
        my_user = self.get_object()

        if 'remove' in request.POST:
            user_id = request.POST.get('user')
            user = User.objects.get(id = user_id)
          
            if user in my_user.followers.all():

             
                my_user.followers.remove(user)

            if my_user in user.following.all():

                user.following.remove(my_user)

          



        return redirect('user:following', slug=self.request.user.slug)
    


class MemberInGroupView(generic.ListView):

    model = Group
    template_name = 'user/group_member_in.html'
    context_object_name  ='groups'

    def get_success_url(self):
        return reverse_lazy('user:group-member-in', kwargs={'slug': self.object.slug})
    
    def get_queryset(self):

        querySet = Group.objects.filter(
        
            Q(member = self.request.user) 
           
        )
        return querySet

    def get_object(self, queryset=None):
        user_slug = self.kwargs.get('slug')
        group = get_object_or_404(User, slug=user_slug)
        return group
    
    def get_context_data(self, **kwargs: Any):
        

        context = super().get_context_data(**kwargs)

        context['group_requests'] = Group.objects.filter(
            Q(admins_request = self.request.user)|
            Q(moderator_request = self.request.user)
        )

        return context
  
    
