from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Message
from .serializers import ChatMessageSerializer


class ChatMessageListCreate(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user).order_by("date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        deleted_count = queryset.delete()[
            0
        ]  # delete() returns a tuple (count, details)
        return Response(
            {"message": f"{deleted_count} messages deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
