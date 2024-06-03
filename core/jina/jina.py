import requests
import os

from config.settings.base import JINA_API_KEY, \
        JINA_API_URL, \
        FUNCTIONALITY_CLF_PROMPT_PATH, \
        INTENT_PROMPT_PATH, ORDER_CATEGORIZATION_PROMPT_PATH, \
        FACTUALIT_PROMPT_PATH, YESNO_CATEGORIZATION_PROMPT_PATH, \
        NON_FACTUAL_CATEGORIZATION_PROMPT_PATH, FACTUAL_CATEGORIZATION_PROMPT_PATH, \
        TIMING_REQ_CATEGORIZATION_PROMPT_PATH

class JinaBot:
    def __init__(self):
        
        self.prompt_user_key = "$USER_MESSAGE"

    
    def __request(self, prompt):
        data = {
            "messages": [
                {
                "role": "user",
                "content": prompt
                }
            ]
        }

        response = requests.post(
        JINA_API_URL,
        headers={
            "authorization": f"Bearer {JINA_API_KEY}",
            "content-type": "application/json"
        },
        json=data
        )

        result = response.json()
        return result
         
    def __extract_assistant_content(self, data):
        # Check if the key 'choices' exists and if it has at least one item
        if 'choices' in data and len(data['choices']) > 0:
            for choice in data['choices']:
                # Check if 'message' key exists, and if 'role' is 'assistant'
                if 'message' in choice and choice['message']['role'] == 'assistant':
                    return choice['message']['content']
        return None 

    def __load_template(self, path):
        with open(path, 'r') as f:
            template = f.read()
        return template
    
    def __perform_action(self, template_path, user_message):
        template = self.__load_template(template_path)
        prompt = template.replace(self.prompt_user_key, user_message)
        result = self.__request(prompt)
        return self.__extract_assistant_content(result).lower()
    
    #functionality identifier
    def exctract_functionality(self, user_message):
        return self.__perform_action(FUNCTIONALITY_CLF_PROMPT_PATH, user_message)

    def extract_intent_type(self, user_message):
        return self.__perform_action(INTENT_PROMPT_PATH, user_message)
    
    def factuality_separate(self, user_message):
        return self.__perform_action(FACTUALIT_PROMPT_PATH, user_message)
    
    def non_factual_categorize(self, user_message):
        return self.__perform_action(NON_FACTUAL_CATEGORIZATION_PROMPT_PATH, user_message)

    def factual_categorize(self, user_message):
        return self.__perform_action(FACTUAL_CATEGORIZATION_PROMPT_PATH, user_message)
    
    def yes_no_categorize(self, user_message):
        return self.__perform_action(YESNO_CATEGORIZATION_PROMPT_PATH, user_message)
    
    def order_categorize(self, user_message):
        return self.__perform_action(ORDER_CATEGORIZATION_PROMPT_PATH, user_message)

    def timing_request_categorize(self, user_message):
        return self.__perform_action(TIMING_REQ_CATEGORIZATION_PROMPT_PATH, user_message) 
    
    def extract_events_from_sentnece(self, user_message):
        return self.__perform_action(EVENT_EXTRACTION_PROMPT_PATH, user_message)
    
