import os


from core.jina.jina import JinaBot
from core.llama.llama import Llama
from core.alpaca_lora.alpaca_lora import AlpacaLora
from core.mpt30b.mpt30b import MPT
from core.weather.weather import Weather
from core.calendar.calendar import Calendar
from core.utils import get_location_and_time, detect_day1
from config.settings.base import HELP_RESPONSE_PATH
from chat.models import Message
class ChatBot:
    def __init__(self, user, conversation=[], dictionary='') -> None:
        with open(HELP_RESPONSE_PATH, 'r') as f:
            self.help_response = f.read()
        
        self.conversation = conversation
        self.dictionary = dictionary
        self.user = user

        self.functionality_identifier = Llama()
        self.intent_classifier = Llama()
        self.greet = Llama()
        self.question_categorizer = Llama()
        self.factuality_separator = JinaBot()
        self.non_factual_categorizer = JinaBot()
        self.yes_no_categorizer = JinaBot()
        self.order_categorizer = JinaBot()
        self.time_request_categorizer = JinaBot()
        self.event_extractor = AlpacaLora()

    def __create_joke(self, message):
        llama = Llama()
        prev_jokes = Message.objects.filter(owner=self.user, source="bot", type="joke")
        prev_jokes = [p.text for p in prev_jokes][- min(len(prev_jokes), 5):]
        return llama.create_joke(message, previous_jokes=prev_jokes), "joke"
    
    def __create_recipe(self, message):
        mpt = MPT()
        return mpt.query(message, self.conversation[-min(10, len(self.conversation)):]), "other"
    
    def __report_weather(self, message):

        return Weather().get_weather(message), "weather"

    def __report_time(self, message):
        category = self.time_request_categorizer.timing_request_categorize(message)
        if 'day or date request' in category:
            return detect_day1(message), "other"
        else:
            return get_location_and_time(), "other"
    
    def __other_inquiry(self, message):
        mpt = MPT()
        return mpt.query(message, self.conversation[-min(10, len(self.conversation)):]), "other"
    
    def __calendar_request(self, message):
        response = self.event_extractor.extract_events(message)
        response = response.lower()
        response = response.strip('{}') 
        response = response.split(',') 

        dictionary_data = {}
        for split in response:
            key, value = map(str.strip, split.split(':')) # diviser par deux points et supprimer les espaces supplémentaires
            if value: # ajouter seulement la paire clé-valeur au dictionnaire si la valeur n'est pas vide
                dictionary_data[key] = value
        calendar = Calendar(dictionary_data)

        response, completed = calendar.add_event(message)
        if not completed:
            self.dictionary = self.dictionary + ' ' + message
        
        return response
    
    def __grocery_list(self, message):
        return "grocery changes done."
    
    def __question_answer(self, message):
        question_category = self.question_categorizer.question_categorize(message)
        if "weather request" in question_category:
            return self.__report_weather(message)
        elif "joke request" in question_category:
            return self.__create_joke(message)
        elif "timing request" in question_category:
            return self.__report_time(message)
        elif "recipe request" in question_category:
            return self.__create_recipe(message)
        else:
            return self.__other_inquiry(message)

    def __yes_no_answer(self, message):
        return self.__question_answer(message)
    
    def __order_answer(self, message):
        question_category = self.order_categorizer.order_categorize(message)
        if "joke request" in question_category:
            return self.__create_joke(message)
        elif "calendar request" in question_category:
            return self.__calendar_request(message)
        elif "grocery list" in question_category:
            return self.__grocery_list(message)
        else:
            return self.__question_answer(message)
        
    def __greeting(self, message):
        return self.greet.greet(message), "other"
    

    def answer(self, message):
        inquiry_type = self.functionality_identifier.exctract_functionality(message)
        
        print(inquiry_type)
        # no prev request ongoing
        if self.dictionary == '':
            if "functionality query" in inquiry_type:
                return self.help_response, "other"
            else:
                intent_type = self.intent_classifier.extract_intent_type(message)
                if "asking a question" in intent_type:
                    response = self.__question_answer(message)
                if "greeting" in intent_type:
                    response = self.__greeting(message)
                elif "statement" in intent_type:
                    response = self.__order_answer(message)
                
                elif "apology" in intent_type or "feedback" in intent_type:
                    response = self.__other_inquiry(message)
            return response
                
        else:
            #TODO
            #resume the calendar or grocery requests
            pass
            return "ELSE", "other"
        