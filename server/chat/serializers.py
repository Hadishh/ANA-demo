from rest_framework import serializers
from .models import Message

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'owner', 'source', 'text', 'date']
        read_only_fields = ['owner']