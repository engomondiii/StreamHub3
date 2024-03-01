import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mediaManager.models import Album, Media, Comment, Like, AlbumTag, MediaTag
from User.models import CustomUser, UserTag
from chat.models import Chat, Message

from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populate models with sample data'

    def handle(self, *args, **kwargs):
        tags = ["joy","space","family","love","nature","work"]
        # Create sample tags for albums
        album_tags = []
        for tag in tags:
            album_tag = AlbumTag.objects.create(value=tag)
            album_tags.append(album_tag)

        # Create sample tags for media
        media_tags = []
        for tag in tags:
            media_tag = MediaTag.objects.create(value=tag)
            media_tags.append(media_tag)
            # Create sample tags for Users
        user_tags = []
        for tag in tags:
            user_tag = UserTag.objects.create(value=tag)
            user_tags.append(user_tag)

        # Create sample users
        User = get_user_model()
        users = []
        for i in range(10):
            user = CustomUser.objects.create_user(
                username=f'user{i+1}',
                email=f'user{i+1}@gmail.com',
                password='12345',
                bio=f'User bio {i+1}',
                full_name=f'User {i+1} Full Name',
                devices=f'Device {i+1}',
            )
            tag_values = random.sample(user_tags, random.randint(1, len(user_tags)))
            user.tags.add(*tag_values)
            users.append(user)

        # Create sample albums
        albums = []
        for i in range(5):
            album = Album.objects.create(
                title=f'Album {i+1}',
                user=random.choice(users),
                privacy=random.choice(['public', 'private', 'subscribers']),
            )
            album.tags.add(*random.sample(album_tags, random.randint(1, len(album_tags))))
            albums.append(album)

        # Specify the path to the folder containing image files
        image_folder = r'c:\Users\karan\Desktop\vision api\media'

        # List all image files in the folder
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]
        # image_path = r'C:\Users\karan\OneDrive\Documents\GitHub\StreamHub-backend\backend\StreamHubBackend\media\uploads'
        # Create sample media using image files
        for i, image_file in enumerate(image_files):
            media = Media.objects.create(
                title=f'Media {i+1}',
                description=f'Description for Media {i+1}',
                privacy=random.choice(['public', 'private', 'subscribers']),
                file=image_file,
                album=random.choice(albums),
                user=random.choice(users),
            )
            media.tags.add(*random.sample(media_tags, random.randint(1, len(media_tags))))
            # Create sample chats and messages
            chats = []
            for i in range(3):  # Creating 3 sample chats
                chat = Chat.objects.create()
                participants = random.sample(users, random.randint(2, 5))
                chat.participants.add(*participants)

                for j in range(10):  # Adding 10 messages to each chat
                    sender = random.choice(participants)
                    recipient = random.choice(participants)  # Choose a random recipient from
                    content = f'Message {j+1} in Chat {i+1}'
                    timestamp = timezone.now() - timezone.timedelta(days=random.randint(1, 30))
                    message = Message.objects.create(chat=chat, sender=sender,recipient=recipient, content=content, timestamp=timestamp)
                chats.append(chat)
            # Create sample likes for each media
            for _ in range(random.randint(1, 5)):
                like = Like.objects.create(
                    user=random.choice(users),
                    value=random.choice(['like', 'dislike']),
                )
                media.likes.add(like)
             # Create sample chats and messages
       
                # Create sample comments for each media
            for _ in range(random.randint(1, 10)):
                comment = Comment.objects.create(
                    user=random.choice(users),
                    content=f'Comment for Media {i+1}',
                )
                media.comments.add(comment)

                # Associate the comment with a random chat
                chat = random.choice(chats)
                comment.chats.add(chat)



        self.stdout.write(self.style.SUCCESS('Sample data populated successfully.'))
