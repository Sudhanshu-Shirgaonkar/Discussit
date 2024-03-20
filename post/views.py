from django.shortcuts import render
from typing import Any, Dict
from django.shortcuts import render,redirect
from django.views import generic
from .models import Post,Comment,Reply
from .forms import CreateTextBasedPostForm,CreateImageBasedPostForm,CreateVideoBasedPostForm,CommentForm,ReplyForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from group.models import Group
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Count,Sum
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.



class PostView(generic.DetailView):

    template_name = 'post/post.html'
    model = Post

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Fetch the objects based on the two slug fields
        group = Group.objects.get(slug=self.kwargs['slug'])
        post = Post.objects.get(slug=self.kwargs['slug2'])

        # Annotate the comment queryset with the number of replies
        comments = Comment.objects.filter(post=post).annotate(num_replies=Count('reply'))

        # Return a dictionary containing both objects
        return {'group': group, 'post': post,'comments': comments}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        post = obj['post']
        comments = obj['comments']

        # Sum the counts of comments and replies
        comment_count = comments.aggregate(num_comments=Sum('num_replies') + Count('id'))['num_comments']

        # Pass the objects to the template context
        context['post'] = post
        context['group'] = obj['group']

        if self.request.GET.get('sortby') == 'like':
            context['comments'] = comments.annotate(num_upvotes=Count('upvotes')).order_by('-num_upvotes', '-created_at')
        else:
            context['comments'] = comments.order_by("-created_at")

        context['comment_count'] = comment_count
        context['form'] = CommentForm()

        return context
    
    def post(self, request, *args, **kwargs):
        # Get the Post and Group objects
        group = Group.objects.get(slug=self.kwargs['slug'])
        post = Post.objects.get(slug=self.kwargs['slug2'])

        # Create a new instance of the CommentForm with the POST data
        form = CommentForm(request.POST)

        if form.is_valid():
            # Create a new Comment object and set its attributes
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            # Redirect to the post detail view
            return redirect(reverse_lazy('post:post', kwargs={'slug': group.slug, 'slug2': post.slug}))
        else:
            # If the form is not valid, render the post detail view with errors
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)






class CreateTextBasedPost(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):
    template_name = 'post/post_create_text.html'
    model = Post
    form_class = CreateTextBasedPostForm
    success_message = 'Post Created Successfully'
   
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs) 
        context['slug'] = self.kwargs.get('slug')
        context['group'] = Group.objects.get(slug=context['slug']) 
        return context
    
    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        group = Group.objects.get(slug = slug)
        post = form.save(commit=False)
          # Save the post object first

        if group.approve_post== True:
      
            post.is_approved = False

        post.group = group
        post.is_text_based = True
        post.author = self.request.user
     
        post.save()
        self.object = post 
        return super().form_valid(form)

    def get_success_url(self):
        group = self.get_context_data()['group']  

      
        if self.object.is_approved:
            return reverse_lazy('post:post',kwargs={'slug': group.slug, 'slug2': self.object.slug})
            
        else:
            return reverse_lazy('user:submitted-post', kwargs={'slug': self.object.slug})
        
        
    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        group = Group.objects.get(slug=slug)

        if group.allow_text_posts:
            return super().dispatch(request, *args, **kwargs)
            
        
        elif group.allow_image_posts:
            return redirect(reverse_lazy('post:create-image-post', kwargs={'slug': slug}))
        
        elif group.allow_video_posts:
            return redirect(reverse_lazy('post:create-video-post', kwargs={'slug': slug}))
            
        
         

       

class CreateImageBasedPost(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):
    template_name = 'post/post_create_image.html'
    model = Post
    form_class = CreateImageBasedPostForm
    success_message = 'Post Created Successfully'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs) 
        context['slug'] = self.kwargs.get('slug')
        context['group'] = Group.objects.get(slug=context['slug']) 
        return context
    
    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        group = Group.objects.get(slug = slug)
        post = form.save(commit=False)
          # Save the post object first
        if group.approve_post == True:
            post.is_approved = False
        post.group = group
   
        post.is_image_based = True
        post.author = self.request.user
     
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        group = self.get_context_data()['group']  

        post = self.object

        if post.is_approved:
            return reverse_lazy('post:post',kwargs={'slug': group.slug, 'slug2': self.object.slug})
            
        else:
            return reverse_lazy('user:submitted-post', kwargs={'slug': post.slug})
        
    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        group = Group.objects.get(slug=slug)

        if group.allow_image_posts:
            return super().dispatch(request, *args, **kwargs)
            
        
        elif group.allow_text_posts:
            return redirect(reverse_lazy('post:create-text-post', kwargs={'slug': slug}))
        
        elif group.allow_video_posts:
            return redirect(reverse_lazy('post:create-video-post', kwargs={'slug': slug}))
        
    

class CreateVideoBasedPost(LoginRequiredMixin,SuccessMessageMixin,generic.CreateView):
    template_name = 'post/post_create_video.html'
    model = Post
    form_class = CreateVideoBasedPostForm
    success_message = 'Post Created Successfully'
   
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs) 
        context['slug'] = self.kwargs.get('slug')
        context['group'] = Group.objects.get(slug=context['slug']) 
        return context
    
    def form_valid(self, form):
        slug = self.kwargs.get('slug')
        group = Group.objects.get(slug = slug)
        post = form.save(commit=False)
          # Save the post object first

        if group.approve_post== True:
         
            post.is_approved = False
        post.group = group
        post.is_video_based = True
        post.author = self.request.user
     
        post.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        group = self.get_context_data()['group']  

        post = self.object

        if post.is_approved:
            return reverse_lazy('post:post',kwargs={'slug': group.slug, 'slug2': self.object.slug})
            
        else:
            return reverse_lazy('user:submitted-post', kwargs={'slug': post.slug})

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        group = Group.objects.get(slug=slug)

        if group.allow_video_posts:
            return super().dispatch(request, *args, **kwargs)
            
        
        elif group.allow_image_posts:
            return redirect(reverse_lazy('post:create-image-post', kwargs={'slug': slug}))
        
        elif group.allow_text_posts:
            return redirect(reverse_lazy('post:create-text-post', kwargs={'slug': slug}))
        

       
            
    

class DeletePostView(LoginRequiredMixin, SuccessMessageMixin,generic.DeleteView):
    model = Post
    success_message = "Post Deleted"

    def get_success_url(self):
        post = self.object
        if post.is_approved:
            return reverse_lazy('group:group', kwargs={'slug':post.group.slug})
        else:
            return self.request.META.get('HTTP_REFERER', '/')
        

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request,"Post deleted Successfully")
        return HttpResponseRedirect(self.get_success_url())
    

class UpdatePostView(LoginRequiredMixin,SuccessMessageMixin, generic.UpdateView):
    model = Post
    template_name = 'post/update.html'
    success_message = "Post updated"


    def get_success_url(self):
        post = self.object


        if post.is_approved:
            return reverse_lazy('post:post', kwargs={'slug':post.group.slug,'slug2': post.slug})
        else:
            return reverse_lazy('user:submitted-post', kwargs={'slug': self.request.user.slug})

    def get_form_class(self):
        post = self.object
        if post.is_text_based == True:
            return CreateTextBasedPostForm
        
        elif post.is_image_based == True:
            return CreateImageBasedPostForm
        
        else:
            return CreateVideoBasedPostForm





class DeleteCommentView(LoginRequiredMixin,SuccessMessageMixin,generic.DeleteView):
    model = Comment
    success_message = 'Comment deleted'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def get(self, request, *args, **kwargs):
        referer = request.META.get('HTTP_REFERER', '/')
        self.object = self.get_object()
        comment = self.object

        if '/reply' in referer:
            messages.success(request, f"Comment was deleted")
            url = reverse_lazy('post:post', kwargs={'slug': comment.post.group.slug, 'slug2': comment.post.slug})
            self.object.delete()
            return HttpResponseRedirect(url)
        
        
        self.object.delete()
        messages.success(request, f"Comment was deleted")
        return HttpResponseRedirect(self.get_success_url())
    
    
class UpdateCommentView(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView):

    model = Comment
    template_name = 'post/update_comment.html'
    form_class = CommentForm
    success_message = "Comment Updated"

    def get_success_url(self):
        # Get the post and group slugs from the URL
        group_slug = self.kwargs.get('slug')
        post_slug = self.kwargs.get('slug2')
        
        success_url = reverse_lazy('post:post', kwargs={'slug': group_slug, 'slug2': post_slug})
        return success_url
    




class ReplyView(SuccessMessageMixin,generic.DetailView):

    template_name = 'post/reply.html'
    model = Post
    

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        # Fetch the objects based on the two slug fields
        group = Group.objects.get(slug=self.kwargs['slug'])
        comment = Comment.objects.get(id=self.kwargs['pk'])
        try:
            # reply = Reply.objects.filter(comment=comment).order_by("-created_at")
            reply = Reply.objects.filter(comment=comment).order_by("created_at")
        except:
            reply = None

        print(reply)
        print(comment)
        # Return a dictionary containing both objects
        return {'group': group, 'comment': comment,'reply':reply}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the objects to the template context
        context['comment'] = self.object['comment']
        context['group'] = self.object['group']
        context['replys'] = self.object['reply']
        context['form'] = ReplyForm()
   

        return context
    
    def post(self, request, *args, **kwargs):

        # Get the Post and Group objects
        group = Group.objects.get(slug=self.kwargs['slug'])
        post = Post.objects.get(slug=self.kwargs['slug2'])
        comment= Comment.objects.get(id=self.kwargs['pk'])

        # Create a new instance of the CommentForm with the POST data
        form = ReplyForm(request.POST)

        if form.is_valid():
            # Create a new Comment object and set its attributes
            reply = form.save(commit=False)
            reply.author = request.user
            reply.comment = comment
            reply.save()

            # Redirect to the post detail view
            return redirect(reverse_lazy('post:reply', kwargs={'slug': group.slug, 'slug2': post.slug,'pk':comment.id}))
        else:
            # If the form is not valid, render the post detail view with errors
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
        

class UpdateReplyView(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView):

    model = Reply
    template_name = 'post/update_comment.html'
    form_class = ReplyForm
    success_message = 'Reply Updated'

    def get_success_url(self):
        # Get the post and group slugs from the URL
        group_slug = self.kwargs.get('slug')
        post_slug = self.kwargs.get('slug2')
        comment_id = self.kwargs.get('pk2')
        
        success_url = reverse_lazy('post:reply', kwargs={'slug': group_slug, 'slug2': post_slug,'pk':comment_id})
        return success_url
    

class DeleteReplyView(LoginRequiredMixin,SuccessMessageMixin,generic.DeleteView):
    model =Reply
    success_message = "Reply Deleted"

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, f"Reply was deleted")
        return HttpResponseRedirect(self.get_success_url())

        

@login_required
def upvote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if not request.user.is_authenticated:
        print("True")

    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
    else:
        post.upvote(request.user)
    return redirect(request.META.get('HTTP_REFERER', ''))

@login_required
def downvote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not request.user.is_authenticated:
        return redirect('account:login')
        
    if request.user in post.downvotes.all():
        post.downvotes.remove(request.user)

    else:
        post.downvote(request.user)
        
    return redirect(request.META.get('HTTP_REFERER', ''))

@login_required
def upvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user in comment.upvotes.all():
        comment.upvotes.remove(request.user)
    else:
        comment.upvote(request.user)
    return redirect(request.META.get('HTTP_REFERER', ''))

@login_required
def downvote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user in comment.downvotes.all():
        comment.downvotes.remove(request.user)

    else:
        comment.downvote(request.user)
    return redirect(request.META.get('HTTP_REFERER', ''))




@login_required
def upvote_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user in reply.upvotes.all():
        reply.upvotes.remove(request.user)
    else:
        reply.upvote(request.user)
    return redirect(request.META.get('HTTP_REFERER', ''))

@login_required
def downvote_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user in reply.downvotes.all():
        reply.downvotes.remove(request.user)

    else:
        reply.downvote(request.user)
    return redirect(request.META.get('HTTP_REFERER', ''))
    
    
    
    