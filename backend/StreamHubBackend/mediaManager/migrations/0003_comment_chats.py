# Generated by Django 4.2.4 on 2024-02-19 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        ('mediaManager', '0002_album_color_album_icon_alter_media_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='chats',
            field=models.ManyToManyField(blank=True, related_name='comment_chats', to='chat.chat'),
        ),
    ]
