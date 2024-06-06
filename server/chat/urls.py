from django.urls import path
from .views import ChatMessageListCreate

urlpatterns = [
    path('chat-history/', ChatMessageListCreate.as_view(), name='chat-history'),
]
