from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView

class ChatView(TemplateView):
    template_name: str = "chat/chat.html"