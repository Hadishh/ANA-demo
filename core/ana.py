import os


from core.jina.jina import JinaBot
from core.mpt30b.mpt30b import MPT
from core.weather.weather import Weather
from core.utils import get_location_and_time, detect_day1
from config.settings.base import HELP_RESPONSE_PATH

class ChatBot:
    def __init__(self, conversation=[]) -> None:
        with open(HELP_RESPONSE_PATH, 'r') as f:
            self.help_response = f.read()
        
        self.conversation = conversation

        self.functionality_identifier = JinaBot()
        self.intent_classifier = JinaBot()
        self.factuality_separator = JinaBot()
        self.non_factual_categorizer = JinaBot()
        self.factual_categorizer = JinaBot()
        self.yes_no_categorizer = JinaBot()
        self.order_categorizer = JinaBot()
        self.time_request_categorizer = JinaBot()

    def __create_joke(self, message):
        mpt = MPT()
        return mpt.query(message, self.conversation[-10:])
    
    def __create_recipe(self, message):
        mpt = MPT()
        return mpt.query(message, self.conversation[-10:])
    
    def __report_weather(self, message):
        return Weather().get_weather(message)

    def __report_time(self, message):
        category = self.time_request_categorizer.timing_request_categorize(message)
        if 'day or date request' in category:
            return detect_day1(message)
        else:
            return get_location_and_time()
    
    def __other_inquiry(self, message):
        mpt = MPT()
        return mpt.query(message, self.conversation[-10:])
    
    def __calendar_request(self, message):
        return "reminder set"
    
    def __grocery_list(self, message):
        return "grocery changes done."
    
    def __factual_answer(self, message):
        question_category = self.factual_categorizer.factual_categorize(message)
        if "wather request" in question_category:
            return self.__report_weather(message)
        elif "timing request" in question_category:
            return self.__report_time(message)
        elif "recipe request" in question_category:
            return self.__create_recipe(message)
        else:
            return self.__other_inquiry(message)
    
    def __non_factual_answer(self, message):
        question_category = self.non_factual_categorizer.non_factual_categorize(message)
        if "joke request" in question_category:
            return self.__create_joke(message)
        elif "weather request" in question_category:
            return self.__report_weather(message)
        elif "timing request" in question_category:
            return self.__report_time(message)
        else:
            return self.__other_inquiry(message)

    def __yes_no_answer(self, message):
        return self.__factual_answer(message)
    
    def __order_answer(self, message):
        question_category = self.order_categorizer.order_categorize(message)
        if "joke request" in question_category:
            return self.__create_joke(message)
        elif "calendar request" in question_category:
            return self.__calendar_request(message)
        elif "grocery list" in question_category:
            return self.__grocery_list(message)
        else:
            return self.__factual_answer(message)
        
    def __greeting(self, message):
        return self.__other_inquiry(self, message)
    

    def answer(self, message, dictionary):
        inquiry_type = self.functionality_identifier.exctract_functionality(message)
        

        # no prev request ongoing
        if dictionary == '':
            if "functionality query" in inquiry_type:
                return self.help_response, dictionary
            else:
                intent_type = self.intent_classifier.extract_intent_type(message)
                if "factual question" in intent_type:                    
                    #WEIRD
                    factuality = self.factuality_separator.factuality_separate(message)
                    if 'not factual question' in factuality:
                        response = self.__non_factual_answer(message)
                        
                    # factual question
                    else:
                        response = self.__factual_answer(message)
                
                # yes no questions
                elif "yes/no question" in intent_type:
                    response = self.__yes_no_answer(message)
                # Orders
                elif 'direct order' in intent_type or 'indirect order' in intent_type:
                    response = self.__order_answer(message)

                elif "greeting" in intent_type:
                    response = self.__greeting(message)
                
                elif "statement" in intent_type:
                    response = self.__order_answer(message)
                
                elif "apology" in intent_type or "feedback" in intent_type:
                    response = self.__other_inquiry(message)
                
        else:
            #TODO
            #resume the calendar or grocery requests
            pass
        return inquiry_type
        