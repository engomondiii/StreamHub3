# account_settings/serializers.py

from rest_framework import serializers
from .models import UserPreferences

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'
