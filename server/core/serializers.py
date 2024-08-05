# explorer/serializers.py

from rest_framework import serializers
from .models import Prompts


class PromptsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Prompts
        fields = "__all__"
