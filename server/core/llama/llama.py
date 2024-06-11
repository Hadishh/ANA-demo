import requests

from datetime import datetime
import pytz

from config.settings.base import JINA_API_KEY, \
        LLAMA_API_URL, \
        FUNCTIONALITY_CLF_PROMPT_PATH, GREETING_PROMPT, \
        INTENT_PROMPT_PATH, ORDER_CATEGORIZATION_PROMPT_PATH, \
        FACTUALIT_PROMPT_PATH, YESNO_CATEGORIZATION_PROMPT_PATH, \
        NON_FACTUAL_CATEGORIZATION_PROMPT_PATH, QUESTION_CATEGORIZATION_PROMPT_PATH, CREATE_JOKE_PROMPT_PATH, \
        TIMING_REQ_CATEGORIZATION_PROMPT_PATH

class Llama():
    def __init__(self):
        
        self.prompt_user_key = "$USER_MESSAGE"
        self.date_time_now_key = "$DATE_TIME_NOW"
        self.previous_conv_key = "$PREVIOUS_CONVERSATION"
    def __request(self, prompt, config):
        data = {
            "prompt": prompt,
            "config": config
        }

        response = requests.post(LLAMA_API_URL, json=data)

        return response.json()
    
    def __extract_assistant_content(self, data:str):
        data = data.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
        
        return data 
    
    def __load_template(self, path):
        with open(path, 'r') as f:
            template = f.read()
        return template
    
    def __perform_action(self, template_path, user_message, config):
        template = self.__load_template(template_path)
        prompt = template.replace(self.prompt_user_key, user_message)
        result = self.__request(prompt, config)
        result = self.__extract_assistant_content(result['response'])
        return result
    
    def extract_intent_type(self, user_message):
        config = {"max_new_tokens" : 128}
        return self.__perform_action(INTENT_PROMPT_PATH, user_message, config).lower()
    
    def exctract_functionality(self, user_message):
        config = {"max_new_tokens" : 64}
        return self.__perform_action(FUNCTIONALITY_CLF_PROMPT_PATH, user_message, config).lower()
    
    def question_categorize(self, user_message):
        config = {"max_new_tokens" : 64}
        return self.__perform_action(QUESTION_CATEGORIZATION_PROMPT_PATH, user_message, config).lower()
    
    def create_joke(self, user_message, previous_jokes):
        config = {"max_new_tokens" : 2048}
        template = self.__load_template(CREATE_JOKE_PROMPT_PATH)
        previous_jokes = "\n\n".join(previous_jokes)

        prompt = template.replace(self.prompt_user_key, user_message).replace(self.previous_conv_key, previous_jokes)

        result = self.__request(prompt, config)
        result = self.__extract_assistant_content(result["response"])

        return result
    
    def greet(self, user_message):
        config = {"max_new_tokens" : 1024}
        edmn_tz = pytz.timezone("America/Edmonton")
        now = datetime.now(tz=edmn_tz)
        response = self.__perform_action(GREETING_PROMPT, user_message, config)
        if now.hour < 12 and now.hour > 4:
            replaced_word = "morning"
        elif now.hour >= 12 and now.hour < 18:
            replaced_word = "afternoon"
        else:
            replaced_word = "evening"
        response = response.replace("morning", replaced_word).replace("afternoon", replaced_word).replace("evening", replaced_word)
        
        return response