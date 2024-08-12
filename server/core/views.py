from rest_framework import viewsets, permissions
from .models import Prompts
from .serializers import PromptsSerializers


class PromptViewSet(viewsets.ModelViewSet):
    serializer_class = PromptsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prompts.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
