from django.contrib import admin
from mediaManager.models import Album, Comment,Media
# Register your models here.
admin.site.register(Album)
admin.site.register(Comment)
admin.site.register(Media)