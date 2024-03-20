from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_picture = models.ImageField(default="profile_pics/avatar.svg",upload_to='profile_pics')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='follower_user',blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='following_user',blank=True)
    new_follower = models.BooleanField(default=False)
    RECENT_GROUP_VISITS_LIMIT = 3
    visited_groups = models.ManyToManyField('group.Group', related_name='recent_visitors', blank=True)
    group_notification = models.ManyToManyField('group.Group', related_name='group_notification', blank=True)

    def visit_group(self, group):
        """
        Adds the group to the user's visited_groups.
        If the user has already visited the group, it is moved to the front of the list.
        If the number of visited groups exceeds the limit, the oldest visit is removed.
        """
      
        if self.visited_groups.filter(pk=group.pk).exists():
            self.visited_groups.remove(group)
        self.visited_groups.add(group)
        visits = self.visited_groups.order_by('-recent_visitors__created_at')
        if visits.count() > self.RECENT_GROUP_VISITS_LIMIT:
            oldest_visit = visits.last()
            oldest_visit.recent_visitors.remove(self)
        self.save()

    def save(self, *args, **kwargs):
        from group.models import Group  # Import inside the method
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
