# chat/consumers.py

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .tasks import get_response
from users.models import User
from .models import Message

class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        # The consumer ChatConsumer is synchronous while the channel layer
        # methods are asynchronous. Therefore wrap the methods in async-to-sync
        # async_to_sync(self.channel_layer.send)(
        #     self.channel_name,
        #     {
        #         "type": "chat_message",
        #         "text": {"msg": text_data_json["text"], "source": "user"},
        #     },
        # )

        user = self.scope['user']
        new_message = Message.objects.create(owner=user, text=text_data_json["text"], source="user")
        new_message.save()
        
        get_response(self.channel_name, text_data_json, user)



    # Handles the chat.mesage event i.e. receives messages from the channel layer
    # and sends it back to the client.
    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))