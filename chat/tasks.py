# chat/tasks.py

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from core.ana import ChatBot
channel_layer = get_channel_layer()

@shared_task
def get_response(channel_name, input_data):
    chatbot = ChatBot()
    response = chatbot.answer(input_data)

    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "chat.message",
            "text": {"msg": response, "source": "bot"},
        },
    )