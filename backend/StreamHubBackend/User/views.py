from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ValidationError


@api_view(['GET'])
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def user_create(request):
    if request.method == 'POST':
        print(request.data)
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate a token for the newly created user
            token, created = Token.objects.get_or_create(user=user)

            data = {
                'success': True,
                'message': 'User created successfully',
                'token': token.key,  # Include the token in the response
                'user_id': user.id,  # Include the user ID in the response if needed
                'username': user.username,  # Include other user details if needed
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            'success': False,
            'message': 'User creation failed',
            'errors': serializer.errors,
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user  # Get the currently authenticated user

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    """
    API view to follow another user.
    """
    try:
        username_to_follow = request.data.get('username')
        target_user = CustomUser.objects.get(username=username_to_follow)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    try:
        user.follow(target_user)
        return Response({'message': f'You are now following {username_to_follow}'}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    """
    API view to unfollow another user.
    """
    try:
        username_to_unfollow = request.data.get('username')
        target_user = CustomUser.objects.get(username=username_to_unfollow)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if not user.is_following(target_user):
        return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)

    user.following.remove(target_user)

    return Response({'message': f'You have unfollowed {username_to_unfollow}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    API view to get the profile of the authenticated user.
    """
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    """
    API view to get the list of followers for the authenticated user.
    """
    user = request.user
    followers = user.followers.all()
    print(followers.count())
    serializer = CustomUserSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    """
    API view to get the list of users the authenticated user is following.
    """
    user = request.user
    following = user.following.all()
    print(following.count())
    serializer = CustomUserSerializer(following, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
