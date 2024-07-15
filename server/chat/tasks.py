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

    chatbot = ChatBot(user=user)
    answer, type_ = chatbot.answer(input_data["text"])
    new_message = Message.objects.create(
        owner=user, text=input_data["text"], source="user", type=type_
    )
    new_message.save()
    # answer = "HI HOW CAN I HELP YOU?"
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "chat.message",
            "text": {"msg": answer, "source": "bot", "debug": chatbot.debug_report},
        },
    )
    new_message = Message.objects.create(
        owner=user, text=answer, source="bot", type=type_
    )
    new_message.save()
