from django.shortcuts import render
from account.models import User
from post.models import Post
from group.models import Group
from django.views import generic
from django.db.models import Q
# Create your views here.


class SearchResultsView(generic.ListView):
    model = Post
    template_name = 'search/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        type = self.request.GET.get('type')
        print(type)
        object_list = None
        if type == 'post' or type == None:
            object_list = Post.objects.filter(
                Q(title__icontains=query) |
                Q(author__username__icontains=query)
            )
            self.context_object_name = 'posts'

       
        elif type == 'group':
            object_list = Group.objects.filter(
                Q(name__icontains=query)
            )
            self.context_object_name = 'groups'

        elif type == 'user':
            object_list = User.objects.filter(
                Q(username__icontains=query)
            )
            self.context_object_name = 'users'

        return object_list

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     type = self.request.GET.get('type')
    #     if type == 'post':
    #         context['search_type'] = 'posts'

    #     elif type == 'group':
    #         context['search_type'] = 'Groups'
    #     context['query'] = self.request.GET.get('q')
    #     return context