import spacy
import datetime
from core.alpaca_lora.alpaca_lora import AlpacaLora
from core.calendar.calendar_service import CalendarService

class Calendar:
    def __init__(self, dictionary_data) -> None:
        self.instruction_template = ("Ask a question to the user about the exact {} to put in the calendar")
        self.question_genrator = AlpacaLora()
        self.nlp = spacy.load("en_core_web_sm")

        self.day = dictionary_data.get("day", None)
        self.time = dictionary_data.get("time", None)
        self.event = dictionary_data.get("event", None)
        

    def __has_duration_before_event(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["TIME", "DURATION"]:
                return True
        return False
    
    def __parse_duration(self, duration_str):
        tokens = duration_str.lower().split()
        if len(tokens) == 2 and tokens[1] == "hours":
            return datetime.timedelta(hours=int(tokens[0]))
        if len(tokens) == 2 and tokens[1] == "minutes":
            return datetime.timedelta(minutes=int(tokens[0]))
        # Add more conditions here to handle more duration formats
        return None
    
    def __get_duration_before_event(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["TIME", "DURATION"]:
                duration = ent.text
                return self.__parse_duration(duration)
        return None
    
    def __has_next_date(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "DATE" and "next" in ent.text.lower():
                return True
        return False
    
    def __get_next_day_date(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "DATE" and "next" in ent.text.lower():
                next_day = ent.text.split()[-1]  # Extract the day of the week from the entity text
                return self.__get_next_day(next_day)  # Call the previous code to get the date of the next day
        return None
    
    def __get_next_day(self, day):
        today = datetime.datetime.today()
        weekday_map = {
            "monday": 0,            
            "tuesday": 1, 
            "wednesday": 2, 
            "thursday": 3, 
            "friday": 4, 
            "saturday": 5, 
            "sunday": 6
        }

        days_until_next_day = (weekday_map[day.lower()] - today.weekday()) % 7
        next_day = today + datetime.timedelta(days=days_until_next_day)
        return next_day.strftime("%Y-%m-%d")
    
    def __subtract_duration_from_time(self, time_str, reminder):
        # Parse the time string to a timedelta
        time_td = datetime.timedelta(hours=int(time_str[:2]), minutes=int(time_str[3:5]), seconds=int(time_str[6:]))

        # Parse the duration string to a timedelta
        duration_td = datetime.timedelta(hours=int(reminder[:2]), minutes=int(reminder[3:5]), seconds=int(reminder[6:]))

        # Subtract the duration from the time
        new_time_td = time_td - duration_td

        # Format the new timedelta back to a time string
        new_time_str = str(int(new_time_td.total_seconds() // 3600)).zfill(2) + ':' + str(int((new_time_td.total_seconds() % 3600) // 60)).zfill(2) + ':' + str(int(new_time_td.total_seconds() % 60)).zfill(2)

        return new_time_str
    
    def add_event(self, message):
        event_added = False
        reminder = self.__get_duration_before_event(message)

        if not self.day and not self.time:
            response = self.question_genrator.ask_question(self.instruction_template.format("day and time"), message)
        elif not self.day:
            response = self.question_genrator.ask_question(self.instruction_template.format("day"), message)
        elif not self.time:
            response = self.question_genrator.ask_question(self.instruction_template.format("time"), message)
        elif not reminder:
            response = 'when do you want to be reminded'
        else:
            time_str = self.time + ":00:00"
            new_time_str = self.__subtract_duration_from_time(time_str, reminder)
            day_str = str(self.day)
            today = datetime.today()
            date_str = ''
            if day_str.lower() == 'next week':
                next_week = today + datetime.timedelta(days=7)
                date_str = next_week.strftime('%Y-%m-%d')
            if self.__has_next_date(message):
                next_day_date = self.__get_next_day_date(message)
                date_str = next_day_date
            
            elif day_str.lower() == 'tomorrow':
                next_week = today + datetime.timedelta(days=1)
                date_str = next_week.strftime('%Y-%m-%d')
            elif day_str.lower() == 'today':
                date_str = today.strftime('%Y-%m-%d')
            datetime_str = date_str + ' ' + new_time_str
            new_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

            service = CalendarService()

            service.add_event(self.event, new_time)

            response = "Event Added"
            event_added = True

        return response, event_added

