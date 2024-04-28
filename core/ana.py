import os


from core.jina.jina import JinaBot
from config.settings.base import HELP_RESPONSE_PATH

class ChatBot:
    def __init__(self) -> None:
        with open(HELP_RESPONSE_PATH, 'r') as f:
            self.help_response = f.read()

    def answer(self, message):
        message_text = message["text"]
        inquiry_type = JinaBot().classify_query(message_text).lower()
        if "functionality query" in inquiry_type:
            return self.help_response
        return inquiry_type
        