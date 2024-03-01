# media_populate_script.py
import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from User.models import CustomUser
from mediaManager.models import Media, Album, Comment

class Command(BaseCommand):
    help = 'Populate the Media model with random data and images'

    def handle(self, *args, **options):
        image_folder = r'c:\Users\karan\Desktop\vision api\media'  # Update this with the path to your image folder

        # List all image files in the folder
        image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]

        users = CustomUser.objects.all()
        albums = Album.objects.all()

        for image_file in image_files:
            # Generate random details
            title = f"Random Title {random.randint(1, 100)}"
            description = f"Random Description {random.randint(1, 100)}"
            privacy = random.choice(['public', 'private', 'subscribers'])
            tags = random.choice(['family', 'Space', 'Happy','love','Space'])
            user = random.choice(users)
            album = None

            # Create Media instance
            media_instance = Media(
                title=title,
                description=description,
                privacy=privacy,
                tags=tags,
                user=user,
                album=album,
            )

            # Attach the image file
            with open(os.path.join(image_folder, image_file), 'rb') as f:
                media_instance.file.save(image_file, File(f))

            media_instance.save()

        self.stdout.write(self.style.SUCCESS('Media instances populated successfully.'))
