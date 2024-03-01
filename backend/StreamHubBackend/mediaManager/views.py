import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Album, Media, Like , Comment
from .serializers import AlbumSerializer, MediaSerializer,CommentSerializer, LikeSerializer
from datetime import datetime, timedelta
from .services import ContentRecommendationAlgorithm
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def album_list(request):
    if request.method == 'GET':
        albums = Album.objects.filter(user=request.user)
        paginator = Paginator(albums, 10)  # Change 10 to the desired page size
        page = request.GET.get('page')
        try:
            album_page = paginator.page(page)
        except PageNotAnInteger:
            album_page = paginator.page(1)
        except EmptyPage:
            album_page = paginator.page(paginator.num_pages)
        serializer = AlbumSerializer(album_page, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AlbumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def album_detail(request, album_id):
    try:
        album = Album.objects.get(id=album_id, user=request.user)
    except Album.DoesNotExist:
        return Response({'message': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        album.delete()
        return Response({'message': 'Album deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def media_list(request):
    if request.method == 'GET':
        media_items = Media.objects.filter(user=request.user)
        paginator = Paginator(media_items, 10)  # Change 10 to the desired page size
        page = request.GET.get('page')
        try:
            media_page = paginator.page(page)
        except PageNotAnInteger:
            media_page = paginator.page(1)
        except EmptyPage:
            media_page = paginator.page(paginator.num_pages)
        serializer = MediaSerializer(media_page, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def media_manager(request, media_id):
    try:
        media_item = Media.objects.get(id=media_id, user=request.user)
    except Media.DoesNotExist:
        return Response({'message': 'Media item not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MediaSerializer(media_item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MediaSerializer(media_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        media_item.delete()
        return Response({'message': 'Media item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class MediaDetailsView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve the media object
        media_id = self.kwargs.get('pk')
        try:
            media = Media.objects.get(pk=media_id)
        except Media.DoesNotExist:
            return Response({'error': 'Media not found'}, status=status.HTTP_404_NOT_FOUND)

        # Get comments and likes for the media
        comments = Comment.objects.filter(media_comments__id=media_id)
        likes = Like.objects.filter(media_likes__id=media_id)

        # Serialize comments and likes
        comments_serializer = CommentSerializer(comments, many=True)
        likes_serializer = LikeSerializer(likes, many=True)

        # Return the serialized data
        data = {
            'comments': comments_serializer.data,
            'likes': likes_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    user = request.user  # Assuming user authentication is set up
    recommendation_algorithm = ContentRecommendationAlgorithm(user)

    # Retrieve query parameters from the request
    content_type = request.GET.get('content_type')
    privacy = request.GET.get('privacy')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    recommendations = recommendation_algorithm.get_recommendations(
        content_type=content_type,
        privacy=privacy,
        page=page,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date
    )

    # Convert Album objects to dictionaries
    recommended_albums_dicts = [
        {
            'title': album.title,
            'user': album.user.username,  # Adjust this according to your model structure
            'privacy': album.privacy,
            # Add other fields as needed
        }
        for album in recommendations['recommended_albums']
    ]

    recommendations['recommended_albums'] = recommended_albums_dicts

    # Convert Media objects to dictionaries
    recommended_media_dicts = [
        {
            'title': media.title,
            'description': media.description,
            'privacy': media.privacy,
            'file': media.file.url,  # Assuming 'file' is a FileField
            'album': media.album.title,  # Adjust this according to your model structure
            'user': media.user.username,  # Adjust this according to your model structure
            # Add other fields as needed
        }
        for media in recommendations['recommended_media']
    ]

    recommendations['recommended_media'] = recommended_media_dicts

    # Serialize the data using the custom encoder
    return JsonResponse(recommendations, safe=False, encoder=DjangoJSONEncoder)
