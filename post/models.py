from django.db import models
from account.models import User
from group.models import Group
import random
import string
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.
# Create your models here.



class Post(models.Model):
    group = models.ForeignKey(Group,on_delete= models.CASCADE, null=True,blank= True)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=200,blank=True)
    content = RichTextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(User, related_name='post_upvotes',blank=True)
    downvotes = models.ManyToManyField(User, related_name='post_downvotes',blank=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    is_text_based = models.BooleanField(default=False)
    is_image_based = models.BooleanField(default=False)
    is_video_based = models.BooleanField(default=False)
    is_approved = models.BooleanField(default= True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.clean()
        if not self.slug:
            base_slug = slugify(self.title.lower())
            max_length = self._meta.get_field('slug').max_length

            # generate random suffix until a unique slug is found
            while True:
                suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                if len(base_slug) + len(suffix) <= max_length:
                    self.slug = base_slug + '-' + suffix
                    if not Post.objects.filter(slug=self.slug).exists():
                        break

        super().save(*args, **kwargs)

    def upvote(self, user):
        if not self.upvotes.filter(pk=user.pk).exists():
            self.upvotes.add(user)
            self.downvotes.remove(user) if self.downvotes.filter(pk=user.pk).exists() else None

    def downvote(self, user):
        if not self.downvotes.filter(pk=user.pk).exists():
            self.downvotes.add(user)
            self.upvotes.remove(user) if self.upvotes.filter(pk=user.pk).exists() else None

    def get_votes_count(self):
        return self.upvotes.count() - self.downvotes.count()

 

    class Meta:
        ordering = ['-created_at']









class Comment(models.Model):

    comment= RichTextField(blank=True)
    slug = models.CharField(max_length=200,blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post_date = models.DateTimeField(auto_now=True)
    post =  models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='comment_upvotes',blank=True)
    downvotes = models.ManyToManyField(User, related_name='comment_downvotes',blank=True)
    


    def __str__(self):

        len_title=75
        if len(self.comment)>len_title:
            titlestring=self.comment[:len_title] + '...'
        else:
            titlestring=self.comment
        return titlestring
    


    def save(self,*args,**kwargs):
        self.clean()
        if not self.slug:
            self.slug = slugify(self.comment.lower())

        

        super(Comment,self).save(*args,**kwargs)

    def upvote(self, user):
        if not self.upvotes.filter(pk=user.pk).exists():
            self.upvotes.add(user)
            self.downvotes.remove(user) if self.downvotes.filter(pk=user.pk).exists() else None

    def downvote(self, user):
        if not self.downvotes.filter(pk=user.pk).exists():
            self.downvotes.add(user)
            self.upvotes.remove(user) if self.upvotes.filter(pk=user.pk).exists() else None

    def get_votes_count(self):
        return self.upvotes.count() - self.downvotes.count()

    class Meta:
        ordering = ['-created_at']






class Reply(models.Model):

    reply= RichTextField(blank=True)
    slug = models.CharField(max_length=200,blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment =  models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='reply_upvotes')
    downvotes = models.ManyToManyField(User, related_name='reply_downvotes')

    def __str__(self):

        len_title=75
        if len(self.reply)>len_title:
            titlestring=self.reply[:len_title] + '...'
        else:
            titlestring=self.reply
        return titlestring
    


    def save(self,*args,**kwargs):
        self.clean()
        if not self.slug:
            self.slug = slugify(self.reply.lower())

        

        super(Reply,self).save(*args,**kwargs)

    def upvote(self, user):
        if not self.upvotes.filter(pk=user.pk).exists():
            self.upvotes.add(user)
            self.downvotes.remove(user) if self.downvotes.filter(pk=user.pk).exists() else None

    def downvote(self, user):
        if not self.downvotes.filter(pk=user.pk).exists():
            self.downvotes.add(user)
            self.upvotes.remove(user) if self.upvotes.filter(pk=user.pk).exists() else None

    def get_votes_count(self):
        return self.upvotes.count() - self.downvotes.count()

    class Meta:
        ordering = ['-created_at']


        