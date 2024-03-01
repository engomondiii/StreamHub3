# chat/urls.py
from django.urls import path
from .views import ChatListCreateView, ChatRetrieveUpdateDestroyView, MessageListCreateView, MessageRetrieveUpdateDestroyView

urlpatterns = [
    # Chat URLs
    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatRetrieveUpdateDestroyView.as_view(), name='chat-detail'),

    # Message URLs
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyView.as_view(), name='message-detail'),
]

