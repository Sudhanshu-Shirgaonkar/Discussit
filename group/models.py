from typing import Iterable, Optional
from django.db import models
from account.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError
# Create your models here.

class Group(models.Model):

    CATEGORY_CHOICES = [
        ('Education','Education'),
         ('Entertainment','Entertainment'),
        ('Food','Food'),
        ('Gaming','Gaming'),
        ('Health and Fitness','Health and Fitness'),
        ('Sports','Sports'),
        ('Technology','Technology'),
        ('Travel','Travel'),
        
        
        
        
    ]

    TYPE_CHOICES = [
        ('Public','Public'),
        ('Restricted','Restricted'),
        ('Private','Private')
    ]

    name = models.CharField(max_length=200,unique=True)
    group_picture = models.ImageField(default="group_pics/group_pic.jpg",upload_to='group_pics')
    cover_picture = models.ImageField(default="cover_pics/cover_pic.jpg",upload_to='cover_pics')
    slug = models.CharField(max_length=200,unique=True,blank=True)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    description = models.TextField()
    group_type = models.CharField(max_length=20,choices=TYPE_CHOICES,default="Private")
    allow_text_posts = models.BooleanField(default=True)
    allow_image_posts = models.BooleanField(default=True)
    allow_video_posts = models.BooleanField(default=True)
    approve_members = models.BooleanField(default=False)
    approve_post = models.BooleanField(default=False)
    admins = models.ManyToManyField(User,related_name='group_admins',blank=True)
    moderator = models.ManyToManyField(User,related_name='group_moderator',blank=True)
    admins_request = models.ManyToManyField(User,related_name='group_admins_request',blank=True)
    moderator_request = models.ManyToManyField(User,related_name='group_moderator_request',blank=True)
    member = models.ManyToManyField(User,related_name='group_members',blank=True)
    approval = models.ManyToManyField(User,related_name='approve_members',blank=True)
    blocked = models.ManyToManyField(User,related_name='blocked_members',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.allow_text_posts and not self.allow_image_posts and not self.allow_video_posts:
            raise ValidationError("At least one type of post should be allowed.")
        
        if self.group_type == 'Private':
            self.approve_members = True
    
    def save(self,*args,**kwargs):
        self.clean()
        if not self.slug:
            self.slug = slugify(self.name.lower())

        self.name = self.name.lower()

        super(Group,self).save(*args,**kwargs)



