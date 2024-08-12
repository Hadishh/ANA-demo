import requests

from datetime import datetime
import pytz
from core.models import Prompts

from config.settings.base import (
    LLAMA_API_URL,
    FUNCTIONALITY_CLF_PROMPT_PATH,
    GREETING_PROMPT,
    WEATHER_PROMPT_PATH,
    INTENT_PROMPT_PATH,
    BOOK_NAME_PROMPT_PATH,
    OTHER_INQUIRY_PROMPT_PATH,
    CONTEXT_PROMPT_PATH,
    QUESTION_CATEGORIZATION_PROMPT_PATH,
    CREATE_JOKE_PROMPT_PATH,
    TIMING_REQ_PROMPT_PATH,
)


class Llama:
    def __init__(self, user):

        self.prompt_user_key = "$USER_MESSAGE"
        self.present_time_key = "$PRESENT_TIME"
        self.previous_conv_key = "$PREVIOUS_CONVERSATION"
        self.user = user

    def __request(self, prompt, config):
        data = {"prompt": prompt, "config": config}

        response = requests.post(LLAMA_API_URL, json=data)

        return response.json()

    def __extract_assistant_content(self, data: str):
        data = data.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()

        return data

    def __load_template(self, name):
        object = Prompts.objects.get(user=self.user, name=name)
        template = object.text
        return template

    def __perform_action(self, template_name, user_message, config):
        template = self.__load_template(template_name)
        prompt = template.replace(self.prompt_user_key, user_message)
        result = self.__request(prompt, config)
        result = self.__extract_assistant_content(result["response"])
        return result

    def __perform_action_with_history(
        self, template_name, user_message, chat_history, config
    ):
        chat_history = [h.replace("\n", "") for h in chat_history]
        chat_history = "\n".join(chat_history)

        template = self.__load_template(template_name)
        prompt = template.replace(self.previous_conv_key, chat_history).replace(
            self.prompt_user_key, user_message
        )
        response = self.__request(prompt, config)
        response = self.__extract_assistant_content(response["response"])
        response = response.strip()
        return response

    def extract_intent_type(self, user_message, chat_history):
        config = {"max_new_tokens": 128}

        return self.__perform_action_with_history(
            "intent_template", user_message, chat_history, config
        ).lower()

    def exctract_functionality(self, user_message):
        config = {"max_new_tokens": 64}
        return self.__perform_action(
            "functionality_template", user_message, config
        ).lower()

    def question_categorize(self, user_message, chat_history):
        config = {"max_new_tokens": 64}
        return self.__perform_action_with_history(
            "question_categories_template", user_message, chat_history, config
        ).lower()

    def create_joke(self, user_message, previous_jokes):
        config = {"max_new_tokens": 2048}
        template = self.__load_template("joke_prompt")
        previous_jokes = "\n\n".join(previous_jokes)

        prompt = template.replace(self.prompt_user_key, user_message).replace(
            self.previous_conv_key, previous_jokes
        )

        result = self.__request(prompt, config)
        result = self.__extract_assistant_content(result["response"])

        return result

    def greet(self, user_message):
        config = {"max_new_tokens": 1024}
        edmn_tz = pytz.timezone("America/Edmonton")
        now = datetime.now(tz=edmn_tz)
        response = self.__perform_action("greet_template", user_message, config)
        if now.hour < 12 and now.hour > 4:
            replaced_word = "morning"
        elif now.hour >= 12 and now.hour < 18:
            replaced_word = "afternoon"
        else:
            replaced_word = "evening"
        response = (
            response.replace("morning", replaced_word)
            .replace("afternoon", replaced_word)
            .replace("evening", replaced_word)
        )

        return response

    def report_weather(self, user_message):
        config = {"max_new_tokens": 256}
        return self.__perform_action("weather_template", user_message, config)

    def extract_book_name(self, user_message):
        config = {"max_new_tokens": 32}
        return self.__perform_action("book_details_template", user_message, config)

    def extract_context(self, user_message, chat_history):
        config = {"max_new_tokens": 1024}
        chat_history = [h.replace("\n", "") for h in chat_history]
        chat_history = "\n".join(chat_history)

        template = self.__load_template("context_extraction_template")
        prompt = template.replace(self.previous_conv_key, chat_history).replace(
            self.prompt_user_key, user_message
        )
        response = self.__request(prompt, config)
        response = self.__extract_assistant_content(response["response"])
        response = response.strip()

        if "@@##" in response:
            response = user_message
        return response

    def report_datetime(self, user_message):
        config = {"max_new_tokens": 1024}
        edmn_tz = pytz.timezone("America/Edmonton")
        now = datetime.now(tz=edmn_tz)
        now = now.strftime("Today is %A, %d of %B.\nCurrent time is %H:%M.")

        template = self.__load_template("timing_request_categories_template")
        prompt = template.replace(self.present_time_key, now).replace(
            self.prompt_user_key, user_message
        )
        response = self.__request(prompt, config)
        response = self.__extract_assistant_content(response["response"])

        return response

    def other_inquiry(self, message, chat_history):
        config = {"max_new_tokens": 2048}

        chat_history = [h.replace("\n", "") for h in chat_history]
        chat_history = "\n".join(chat_history)

        template = self.__load_template("other_inquiry_template")
        prompt = template.replace(self.previous_conv_key, chat_history).replace(
            self.prompt_user_key, message
        )
        response = self.__request(prompt, config)
        response = self.__extract_assistant_content(response["response"])

        return response

    def answer_with_external_info(self, message, chat_history, external_info):
        EXTERNAL_INFO_KEY = "$EXTERNAL_KNOWLEDGE"
        config = {"max_new_tokens": 2048}

        chat_history = [h.replace("\n", "") for h in chat_history]
        chat_history = "\n".join(chat_history)

        template = self.__load_template("ana_v2_answer")
        prompt = template.replace(self.previous_conv_key, chat_history)
        prompt = prompt.replace(EXTERNAL_INFO_KEY, external_info)
        prompt = prompt.replace(self.prompt_user_key, message)

        response = self.__request(prompt, config)
        response = self.__extract_assistant_content(response["response"])

        return response

    def ask_if_answer(self, message, chat_history):
        config = {"max_new_tokens": 32}
        response = self.__perform_action_with_history(
            "ana_v2_ask", message, chat_history, config
        )

        return response.lower()

    def get_function_call(self, message, chat_history):
        config = {"max_new_tokens": 32}

        response = self.__perform_action_with_history(
            "ana_v2_functions", message, chat_history, config
        )

        return response.lower()
