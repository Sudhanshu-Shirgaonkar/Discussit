from django import http
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.urls import  reverse_lazy,reverse
from django.views import generic
from post.models import Post, Comment
from typing import Any, Dict
from django.db.models import Count
from group.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F

# Create your views here.


class IndexView(generic.ListView):
    template_name = "home/index.html"

    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Post.objects.filter(is_approved=True).exclude(group__blocked = self.request.user).exclude(group__group_type = 'Private')
        else:
            queryset = Post.objects.filter(is_approved=True).exclude(group__group_type = 'Private')
        queryset = queryset.annotate(
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
            print("here")
            queryset = queryset.annotate(
                combine =  Count("upvotes",distinct=True)  + F('comment_count'),
             
            ).order_by("-combine")
        

         

            return queryset





        if self.request.GET.get("sortby") == "new":
          
            return queryset.order_by("-created_at")
        

        if self.request.GET.get("feed") == "home":
            if self.request.user.is_authenticated:
                queryset = queryset.filter(
                    is_approved=True, group__member=self.request.user
                )

            else:
                queryset = []

            return queryset

        if self.request.GET.get("category") != None:
            category = self.request.GET.get("category")

            queryset = queryset.filter(is_approved=True, group__category=category)

            return queryset
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)
        group = Group.objects.all()
        top_groups = group.annotate(
                member_count=Count("member", distinct=True)
            ).order_by("-member_count")
            
        context['top_groups'] = top_groups[:5]
       
        return context


class AllGroups(generic.ListView):
    template_name = "home/all_groups.html"
    model = Group
    context_object_name = "groups"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = None
        if self.request.GET.get("q") == None:
            queryset = Group.objects.all()

        else:
            queryset = Group.objects.filter(category=self.request.GET.get("q"))

        return queryset
    
class BlockedGroupView(LoginRequiredMixin,generic.DetailView):
    template_name = 'home/blocked.html'
    model = Group
    context_object_name = 'group'
    

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        user = request.user

        # If user is not in block queryset of the group, redirect to home
        if user not in group.blocked.all():
            return redirect(reverse_lazy('index:index'))

        return super().dispatch(request, *args, **kwargs)
    

class PrivateGroupView(generic.DetailView):
    template_name = 'home/private.html'
    model = Group
    context_object_name = 'group'
    

    def get(self, request, *args, **kwargs):
        group = self.get_object()
        user = request.user
        if user.is_authenticated:
            user.visit_group(group)
        return super().get(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)
        group = self.get_object()
      

        related_groups = Group.objects.filter(
            Q(category = group.category) &
            ~Q(id = group.id)
            )
        context['related_groups'] = related_groups[:5]
      
        return context

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        user = request.user

        if user in group.member.all():
            return redirect(reverse('group:group', kwargs={'slug': group.slug}))

        # If user is not in block queryset of the group, redirect to home
        if group.group_type != 'Private':
            return redirect(reverse_lazy('index:index'))

        return super().dispatch(request, *args, **kwargs)


