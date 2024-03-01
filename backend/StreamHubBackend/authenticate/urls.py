from django.urls import path
from .views import CustomObtainAuthToken, LogoutView,check_authentication

urlpatterns = [
    path('check-authentication/', check_authentication, name='check_authentication'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
