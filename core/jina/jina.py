import requests
import os

from config.settings.base import JINA_API_KEY, \
        JINA_API_URL, \
        FUNCTIONALITY_CLF_PROMPT_PATH, \
        INTENT_PROMPT_PATH, \
        FACTUALIT_PROMPT_PATH

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
        # Recipe request, 
        # Joke request, 
        # Weather request, 
        # Timing request (what time is it/what day is it today), 
        # Other
        return "joke request"

    def factual_categorize(self, user_message):
        return "weather request"
    
    def yes_no_categorize(self, user_message):
        return "weather request"
    
    def order_categorize(self, user_message):
        return "calendar request"
    
    
