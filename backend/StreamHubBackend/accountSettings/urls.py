# account_settings/urls.py

from django.urls import path
from .views import user_preferences

urlpatterns = [
    path('preferences/', user_preferences, name='user_preferences'),
]
