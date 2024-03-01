from django.urls import path
from .views import user_list, user_detail,user_create,follow_user,unfollow_user,get_followers,get_following

urlpatterns = [
    path('api/user-create/', user_create , name='user-create'),
    path('api/user-list/', user_list, name='user-list'),
    path('api/user-manager/', user_detail, name='user-detail'),
    
    path('api/follow/', follow_user, name='follow'),
    path('api/unfollow/', unfollow_user, name='unfollow'),
    path('api/get-followers/',get_followers, name='get-followers'),
    path('api/get-following/',get_following, name='get-following'),
]
