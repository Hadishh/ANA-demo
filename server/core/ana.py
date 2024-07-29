import os
import pytz
from datetime import datetime

from core.llama.llama import Llama
from core.weather.weather import Weather
from core.library.book_reading import BookReader
from core.utils import get_location_and_time, detect_day1
from config.settings.base import HELP_RESPONSE_PATH
from chat.models import Message


class ChatBot:
    def __init__(self, user, conversation=[], dictionary="") -> None:
        with open(HELP_RESPONSE_PATH, "r") as f:
            self.help_response = f.read()

        self.conversation = conversation
        self.dictionary = dictionary
        self.user = user
        self.debug_report = str()

        self.functionality_identifier = Llama()
        self.intent_classifier = Llama()
        self.greet = Llama()
        self.question_categorizer = Llama()
        self.book_names_extractor = Llama()
        self.context_extraction = Llama()

        self.chat_history = []

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
        self.debug_report += f"{reader.book_name, reader.chapter_num}"
        return response, "read book"

    def __other_inquiry(self, message):
        llama = Llama()
        chat_history = Message.objects.filter(owner=self.user).order_by("date")
        chat_history = [
            f"{q.source}:{q.text[:500].replace(':', '.')}" for q in chat_history
        ][-min(len(chat_history), 10) :]

        return llama.other_inquiry(message, chat_history), "other"

    def __question_answer(self, message):
        question_category = self.question_categorizer.question_categorize(
            message, self.chat_history
        )
        if "weather request" in question_category:
            self.debug_report += "Weather"
            return self.__report_weather(message)
        elif "joke request" in question_category:
            self.debug_report += "Joke Request"
            return self.__create_joke(message)
        elif "date or time request" in question_category:
            self.debug_report += "Date/Time Request"
            return self.__report_time(message)
        elif "reading a book" in question_category:
            self.debug_report += "Reading Book ->"
            return self.__read_book(message)
        else:
            self.debug_report += "Other"
            return self.__other_inquiry(message)

    def __order_answer(self, message):
        return self.__question_answer(message)

    def __greeting(self, message):
        return self.greet.greet(message), "other"

    def answer(self, message):
        version = message["version"]
        message = message["text"]
        chat_history = Message.objects.filter(owner=self.user).order_by("date")
        source = lambda x: "ANA" if "bot" in x else "USER"
        chat_history = [
            f"{source(q.source)}:{q.text[:500].replace(':', '.')}" for q in chat_history
        ][-min(len(chat_history), 6) :]
        if version == "v2":
            chatbotv2 = ChatbotV2(chat_history, self.user)
            response = chatbotv2.answer(message)
            self.debug_report = chatbotv2.debug
            return response
        inquiry_type = self.functionality_identifier.exctract_functionality(message)

        print(inquiry_type)
        # no prev request ongoing

        if "functionality query" in inquiry_type:
            self.debug_report = "Functionality Query"
            return self.help_response, "other"
        else:
            intent_type = self.intent_classifier.extract_intent_type(
                message, chat_history
            )
            if "asking a question" in intent_type:
                self.debug_report = "Question -> "
                response = self.__question_answer(message)
            if "greeting" in intent_type:
                self.debug_report = "Greeting"
                response = self.__greeting(message)
            elif "statement" in intent_type or "order" in intent_type:
                self.debug_report = "Statement/Order -> "
                response = self.__order_answer(message)
            elif (
                "apology" in intent_type
                or "feedback" in intent_type
                or "other" in intent_type
            ):
                self.debug_report = "Other -> "
                response = self.__other_inquiry(message)
        return response


from core.date_time.time_by_city import get_city_time
import random


class ChatbotV2:
    def __init__(self, chat_history, user) -> None:
        self.chat_history = chat_history
        self.user = user
        self.debug = str()

    def __exctract_args(self, function_call: str, function_name: str):

        function_call = (
            function_call.replace(function_name, "").replace('"', "").strip()
        )
        if len(function_call) < 2:
            return [""]  # Just the function name, made bugs TODO
        if function_call[0] == "(":
            function_call = function_call[1:]
        if function_call[-1] == ")":
            function_call = function_call[:-1]

        args = function_call.split(",")
        args = [arg.strip() for arg in args]

        return args

    def get_time(self, function_call: str):
        args = self.__exctract_args(function_call, "current_time")
        city_name = args[0]
        return get_city_time(city_name)

    def get_weather(self, function_call: str):
        weather = Weather()
        args = self.__exctract_args(function_call, "weather")
        print(args)
        if len(args) != 2:
            args = " ".join(args)
            return weather.get_weather(args)
        city, day = tuple(args)
        return weather.get_weather_by_city(city, day)

    def get_book_details(self, function_call):
        args = self.__exctract_args(function_call=function_call, function_name="book")
        if len(args) == 2:
            book_name, chapter_num = tuple(args)
            chapter_num = (
                int(chapter_num.strip()) if chapter_num.strip().isdecimal() else -1
            )
        else:
            book_name, chapter_num = "none", -1
        reader = BookReader(book_name, chapter_num, self.user)
        return reader.read_book()

    def get_date(self, function_call):
        args = self.__exctract_args(function_call, function_name="date")

        if len(args) == 1:
            day = args[0]
            return Llama().report_datetime(f"What is the date of {day}?")
        else:
            return Llama().report_datetime(f"What is the date of today?")

    def answer(self, message):
        llama = Llama()
        answer = llama.ask_if_answer(
            message, self.chat_history[-min(len(self.chat_history), 4) :]
        )
        if "no" in answer:
            function_call = llama.get_function_call(
                message, self.chat_history[-min(len(self.chat_history), 4) :]
            )
            self.debug = (
                f"The bot cannot ansewr, doing a function call {function_call}:\n"
            )

            external_info = str()

            if "none" in function_call:
                self.debug += (
                    "Resuming the conversation, none of the function calls can help."
                )
                return llama.other_inquiry(message, self.chat_history), "other"
            elif "current_time" in function_call:
                external_info = self.get_time(function_call)
            elif "weather" in function_call:
                external_info = self.get_weather(function_call)
            elif "book" in function_call:
                return self.get_book_details(function_call), "read book"
            elif "date" in function_call:
                external_info = self.get_date(function_call)

            self.debug += f"\n Got the external info: \n\n{external_info}\n\n Possible responses:\n\n"
            RESPONSES = 3
            responses = []

            for _ in range(RESPONSES):
                new_resp = llama.answer_with_external_info(
                    message, self.chat_history, external_info
                )
                responses.append(new_resp)
            self.debug += "[" + "|||||".join(responses) + "\n]"

            return random.choice(responses), "other"

        elif "yes" in answer:
            self.debug = f"The bot can ansewr, resuming the conversation.\n"
            return llama.other_inquiry(message, self.chat_history), "other"
        return answer, "other"
