from rest_framework import generics, status
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(participants=[self.request.user])

class ChatRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(chat__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
