# chat/tasks.py

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from core.ana import ChatBot
from .models import Message
channel_layer = get_channel_layer()

@shared_task
def get_response(channel_name, input_data, user):
    # conversation = Conversation.objects.all().values()

    # if (len(Dictionary.objects.all()) == 0):
    #     Dictionary.objects.create(id=1, text='')
    #     dictionary = ''
    # else:
    #     dictionary = Dictionary.objects.all().values()[0]['text']
    
    # # chatbot = ChatBot(conversation=conversation, dictionary=dictionary)
    # answer = chatbot.answer(input_data['text'])

    answer = "HI HOW CAN I HELP YOU?"
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "chat.message",
            "text": {"msg": answer, "source": "bot"},
        },
    )

    new_message = Message.objects.create(owner=user, text=answer, source="bot")
    new_message.save()
