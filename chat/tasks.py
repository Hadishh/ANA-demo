# chat/tasks.py

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from core.ana import ChatBot
from .models import Conversation, Dictionary
channel_layer = get_channel_layer()

@shared_task
def get_response(channel_name, input_data):
    conversation = Conversation.objects.all().values()
    chatbot = ChatBot(conversation=conversation)

    if (len(Dictionary.objects.all()) == 0):
        Dictionary.objects.create({"id": 1, "text": ""})
        dictionary = ''
    else:
        dictionary = Dictionary.objects.all().values()[0]['text']
    
    answer, dictionary = chatbot.answer(input_data['text'], dictionary)

    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "chat.message",
            "text": {"msg": answer, "source": "bot"},
        },
    )