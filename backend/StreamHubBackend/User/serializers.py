from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'username', 'email', 'bio', 'terms', 'full_name', 'devices', 'profileImage', 'followers', 'following']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure that 'password' is write-only

    def create(self, validated_data):
        # Hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash the new password if it's included in the update data
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
