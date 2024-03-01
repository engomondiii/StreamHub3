from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os
from django.core.exceptions import ValidationError

def user_profile_image_path(instance, filename):
    # Generate a unique filename based on user's username and a random UUID
    ext = filename.split('.')[-1]
    filename = f"{instance.username}_{uuid.uuid4()}.{ext}"
    return os.path.join('media/uploads/', filename)

class UserTag(models.Model):
    value = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractUser):
    # Add any additional fields you need for your user model
    bio = models.TextField(blank=True)
    terms = models.BooleanField(default=False)
    email = models.EmailField(unique=True)  
    full_name = models.TextField(blank=True, null=True)
    devices = models.CharField(max_length=200, default='none')
    profileImage = models.ImageField(
        null=True, blank=True, default='media/res/default.jpg', upload_to=user_profile_image_path
    )

    # Fields from UserProfile model
    followers = models.ManyToManyField('self', related_name='user_followers', symmetrical=False, blank=True)
    following = models.ManyToManyField('self', related_name='user_following', symmetrical=False, blank=True)

    # Many-to-many relationship with Tag model
    tags = models.ManyToManyField(UserTag, related_name='user_tags', blank=True)

    def follow(self, user_to_follow):
        # Check if the user is trying to follow themselves
        if self == user_to_follow:
            raise ValidationError("Cannot follow yourself.")

        self.following.add(user_to_follow)
        user_to_follow.user_followers.add(self)

    def unfollow(self, user_to_unfollow):
        self.following.remove(user_to_unfollow)
        user_to_unfollow.user_followers.remove(self)

    def is_following(self, user):
        return self.following.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        return self.user_followers.filter(pk=user.pk).exists()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check if the user has any tags
        if not self.tags.exists():
            # Check if there is an existing tag with value 'new'
            existing_tag = UserTag.objects.filter(value='new').first()
            if existing_tag:
                self.tags.add(existing_tag)

    def __str__(self):
        return self.username

