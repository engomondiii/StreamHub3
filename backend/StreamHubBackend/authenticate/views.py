from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_401_UNAUTHORIZED




class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print(request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        print(password , email)
        if email == '' or password == '':
            return Response({'error': 'Please provide both email and password'}, status=200 )
        try:
            user = authenticate(email=email, password=password)
        except Exception as e :
            print(e)
        print(user)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': user.id}, status=200)
        else:
            return Response({'error': 'Invalid email or password'}, status=200)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Print the request details to the console for debugging
        print(f"Request data: {request.data}")
        print(f"Request user: {request.user}")
        print(f"Request auth: {request.auth}")
        
        # Check if the user is authenticated before proceeding
        if request.user.is_authenticated:
            # Delete the user's token
            request.auth.delete()
            return Response({'message': 'Logout successful'})
        else:
            return Response({'message': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    # The user is authenticated if the request passes through the TokenAuthentication and IsAuthenticated classes
    user = request.user
    return Response({'message': f'Authenticated as {user.username}', 'user_id': user.id},status=200)