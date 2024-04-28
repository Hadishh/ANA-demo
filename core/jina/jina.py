import requests
import os

from config.settings.base import JINA_API_KEY, JINA_API_URL, FUNCTIONALITY_CLF_PROMPT_TEMP

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

    def classify_query(self, user_message):
        with open(FUNCTIONALITY_CLF_PROMPT_TEMP, 'r') as f:
            template = f.read()
        prompt = template.replace(self.prompt_user_key, user_message)
        result = self.__request(prompt)
        
        return self.__extract_assistant_content(result).lower()