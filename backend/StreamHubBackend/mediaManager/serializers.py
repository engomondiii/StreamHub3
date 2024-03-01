from rest_framework import serializers
from .models import Album, Media, Comment, Like, AlbumTag, MediaTag
from User.models import CustomUser


class AlbumTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumTag
        fields = '__all__'


class MediaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaTag
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = AlbumTagSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = ['id', 'title','icon','color', 'user', 'privacy', 'tags']


class MediaSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = MediaTagSerializer(many=True)
    likes = LikeSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'privacy', 'tags', 'file', 'likes', 'comments', 'album', 'user']
