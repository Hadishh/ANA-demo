import os
import pytz
from datetime import datetime

from core.llama.llama import Llama
from core.alpaca_lora.alpaca_lora import AlpacaLora
from core.weather.weather import Weather
from core.library.book_reading import BookReader
from core.utils import get_location_and_time, detect_day1
from config.settings.base import HELP_RESPONSE_PATH, BOOKS_ROOT_DIR
from chat.models import Message


class ChatBot:
    def __init__(self, user, conversation=[], dictionary="") -> None:
        with open(HELP_RESPONSE_PATH, "r") as f:
            self.help_response = f.read()

        self.conversation = conversation
        self.dictionary = dictionary
        self.user = user

        self.functionality_identifier = Llama()
        self.intent_classifier = Llama()
        self.greet = Llama()
        self.question_categorizer = Llama()
        self.book_names_extractor = Llama()
        self.context_extraction = Llama()

    def __create_joke(self, message):
        llama = Llama()
        prev_jokes = Message.objects.filter(owner=self.user, source="bot", type="joke")
        prev_jokes = [p.text for p in prev_jokes][-min(len(prev_jokes), 5) :]
        return llama.create_joke(message, previous_jokes=prev_jokes), "joke"

    def __report_weather(self, message):
        weather_info = Weather().get_weather(message)
        llama = Llama()
        return llama.report_weather(weather_info), "weather"

    def __report_time(self, message):
        llama = Llama()
        return llama.report_datetime(message), "other"

    def __read_book(self, message):
        llama = Llama()
        details = llama.extract_book_name(message)
        book_name, chapter_num = tuple(details.split(";"))
        chapter_num = (
            int(chapter_num.strip()) if chapter_num.strip().isdecimal() else -1
        )
        book_name = book_name
        reader = BookReader(book_name, chapter_num, self.user)
        response = reader.read_book()
        return response, "read book"

    def __other_inquiry(self, message):
        llama = Llama()
        chat_history = Message.objects.filter(owner=self.user).order_by("date")
        chat_history = [
            f"{q.source}:{q.text[:500].replace(':', '.')}" for q in chat_history
        ][-min(len(chat_history), 10) :]

        return llama.other_inquiry(message, chat_history), "other"

    def __question_answer(self, message):
        question_category = self.question_categorizer.question_categorize(message)
        if "weather request" in question_category:
            return self.__report_weather(message)
        elif "joke request" in question_category:
            return self.__create_joke(message)
        elif "date or time request" in question_category:
            return self.__report_time(message)
        elif "reading a book" in question_category:
            return self.__read_book(message)
        else:
            return self.__other_inquiry(message)

    def __order_answer(self, message):
        return self.__question_answer(message)

    def __greeting(self, message):
        return self.greet.greet(message), "other"

    def answer(self, message):
        inquiry_type = self.functionality_identifier.exctract_functionality(message)

        print(inquiry_type)
        # no prev request ongoing

        if "functionality query" in inquiry_type:
            return self.help_response, "other"
        else:
            chat_history = Message.objects.filter(owner=self.user).order_by("date")
            chat_history = [
                f"{q.source}:{q.text[:500].replace(':', '.')}" for q in chat_history
            ][-min(len(chat_history), 4) :]

            context = self.context_extraction.extract_context(message, chat_history)
            # message = context
            intent_type = self.intent_classifier.extract_intent_type(message)
            if "asking a question" in intent_type:
                response = self.__question_answer(message)
            if "greeting" in intent_type:
                response = self.__greeting(message)
            elif "statement" in intent_type or "order" in intent_type:
                response = self.__order_answer(message)
            elif (
                "apology" in intent_type
                or "feedback" in intent_type
                or "other" in intent_type
            ):
                response = self.__other_inquiry(message)
        return response
