# Generated by Django 4.2.4 on 2024-02-18 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='user_tags', to='User.tag'),
        ),
    ]
