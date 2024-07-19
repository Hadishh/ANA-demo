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

        user = self.scope["user"]

        get_response(self.channel_name, text_data_json, user)

    # Handles the chat.mesage event i.e. receives messages from the channel layer
    # and sends it back to the client.
    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))
