
import random
import string
from django.db import models
from User.models import CustomUser
from chat.models import Chat

class MediaTag(models.Model):
    value = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

class AlbumTag(models.Model):
    value = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.CharField(max_length=20, choices=[('like', 'Like'), ('dislike', 'Dislike'), ('none', 'None')], default='none')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chats = models.ManyToManyField(Chat, blank=True, related_name='comment_chats')
    def __str__(self):
            return {self.content}
class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    privacy = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private'), ('subscribers', 'Subscribers Only')], default='Public')
    tags = models.ManyToManyField(MediaTag, related_name='user_tags', blank=True)
    file = models.FileField(upload_to='user_uploads/')  # Provide a default value
    likes = models.ManyToManyField(Like, blank=True, related_name='media_likes')
    comments = models.ManyToManyField(Comment, blank=True, related_name='media_comments')
    album = models.ForeignKey('Album', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check if the user has any tags
        if not self.tags.exists():
            # Check if there is an existing tag with value 'new'
            existing_tag = MediaTag.objects.filter(value='new').first()
            if existing_tag:
                self.tags.add(existing_tag)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
def generate_random_color():
    # Generate a random hex color code
    return '#' + ''.join(random.choices(string.hexdigits, k=6))
class Album(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    privacy = models.CharField(
        max_length=20,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('subscribers', 'Subscribers Only')
        ],
        default='Public'
    )
    tags = models.ManyToManyField(AlbumTag, related_name='user_tags', blank=True)
    icon = models.CharField(max_length=30, default='ios-people')
    color = models.CharField(max_length=7, default=generate_random_color)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Set the default value for tags to be the same as the title
        if not self.tags.exists():
            # Check if there is an existing tag with value 'new'
            existing_new_tag, created = AlbumTag.objects.get_or_create(value='new')
            self.tags.add(existing_new_tag)

            # Check if there is an existing tag with the album's title
            title_tag, created = AlbumTag.objects.get_or_create(value=self.title.lower())
            self.tags.add(title_tag)


