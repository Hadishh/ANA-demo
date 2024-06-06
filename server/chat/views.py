from rest_framework import generics, permissions
from .models import Message
from .serializers import ChatMessageSerializer

class ChatMessageListCreate(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user).order_by('date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
