from config.settings.base import ALPACA_URL, EVENT_EXTRACTION_INSTRUCTION_PATH
import requests
import os

class AlpacaLora:
    def __init__(self) -> None:
        pass
    
    def __load_template(self, path):
        with open(path, 'r') as f:
            template = f.read()
        return template
    
    def __perform_action(self, instruction, input_text):
        if os.path.exists(instruction):
            instruction = self.__load_template(instruction)
        else:
            pass

        data = {
            "instruction": instruction,
            "input": input_text,
            "temperature": 0.1,
            "top_p": 0.75,
            "top_k": 40,
            "num_beams": 4,
            "max_new_tokens": 128,
        }

        response = requests.post(ALPACA_URL, json=data)
        return response.json()['data']
    
    def extract_events(self, input_text):
        return self.__perform_action(EVENT_EXTRACTION_INSTRUCTION_PATH, input_text)
    
    def ask_question(self, instruction, input_text):
        return self.__perform_action(instruction, input_text)
    