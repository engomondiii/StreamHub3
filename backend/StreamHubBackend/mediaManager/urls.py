from django.urls import path
from .views import album_list, album_detail, media_list, media_manager,get_recommendations,MediaDetailsView

urlpatterns = [
    path('albums/', album_list, name='album-list'),
    path('albums/<int:album_id>/', album_detail, name='album-detail'),
    path('media/', media_list, name='media-list'),
    path('media_manager/<int:media_id>/', media_manager, name='media-manager'),
    path('media_details/<int:pk>/', MediaDetailsView.as_view(), name='media-details'),
    path('get_recommendations/', get_recommendations, name='get_recommendations'),

]
