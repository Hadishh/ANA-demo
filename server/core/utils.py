import spacy
import requests
import datetime
from dateutil import relativedelta
import pytz
from geotext import GeoText
import re

def detect_day(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    time_indicators = ['morning', 'afternoon', 'evening', 'night','tonight','today']
    for token in doc:
        if token.text.lower() == 'tomorrow':
            next_token = token.nbor()
            

        if token.text.lower() == 'next':
            next_token = token.nbor()
            if next_token.text.lower() == 'day':
                return 'Next day'		
            elif next_token.text.lower() in time_indicators:
                return f'Next {next_token.text.lower()}'
        if token.text.lower() == 'next':
            next_token = token.nbor()
            if next_token.text.lower() == 'week':
                return 'Next week'		
        if token.text.lower() in days_of_week:
            return token.text.capitalize()

    for token in doc:
        if token.text.lower() in days_of_week:
            return token.text.capitalize()  # Return the detected day of the week

        if token.text.lower() in ['today', 'tomorrow']:
            return token.text.capitalize()  # Return relative day reference

        if token.text.lower() == 'next' and token.head.text.lower() in days_of_week:
            next_day = token.head.text.capitalize()
            return f"Next {next_day}"  # Return "Next <day of the week>"

    return None  # Return None if no relevant day is detected


def detect_time(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    time_indicators = ['morning', 'afternoon', 'evening', 'night','tonight','now']

    for token in doc:
        if token.text.lower() in time_indicators:
            return token.text.capitalize()

        if token.ent_type_ == "TIME":
            return token.text.capitalize()  # Return the detected time

        # Check for specific time format, e.g., 2:30 PM
        if ":" in token.text and token.i + 2 < len(doc):
            next_token = doc[token.i + 1]
            if next_token.text.lower() == "pm" or next_token.text.lower() == "am":
                return f"{token.text} {next_token.text.upper()}"

    return None

def get_current_location():
    url = "http://ip-api.com/json"  # IP Geolocation API endpoint
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "success":
        return data["city"]
    else:
        return None

def detect_locations_spacy(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    locations = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:  # GPE represents geopolitical entities, LOC represents cities
            locations.append(ent.text)
    return locations

def detect_locations_geotext(text):
    places = GeoText(text)
    cities = places.cities
    return cities


def get_location_and_time():
    # Get location data
    location_data = requests.get('http://ip-api.com/json').json()
    
    # Get timezone and city
    timezone = location_data['timezone']
    city = location_data['city']

    # Get current time in the timezone
    local_time = datetime.datetime.now(pytz.timezone(timezone))

    # Format the time
    formatted_time = local_time.strftime("%I:%M %p").lstrip("0")

    return f"The current time in '{city}' is {formatted_time}"  

def get_date(day):
    # Map string inputs to number of days from today
    day_mapping = {
        "today": 0,
        "tomorrow": 1,
        "next day": 2,
        # Add more as needed...
    }
    
    if day in day_mapping:
        n = day_mapping[day]
    else:
        return "Invalid input. Please enter 'today', 'tomorrow', or 'next day'."

    # Get the current date and add 'n' days
    date_n_days_ahead = datetime.datetime.today() + datetime.timedelta(days=n)

    # Format the date
    formatted_date = date_n_days_ahead.strftime(f"{day} is %A, %B %d, %Y")

    return formatted_date


# Mapping from weekday name to dateutil's weekday constant
WEEKDAY_MAPPING = {
    "monday": relativedelta.MO,
    "tuesday": relativedelta.TU,
    "wednesday": relativedelta.WE,
    "thursday": relativedelta.TH,
    "friday": relativedelta.FR,
    "saturday": relativedelta.SA,
    "sunday": relativedelta.SU,
}

# Special cases mapping
SPECIAL_CASES = {
    "today": 0,
    "tomorrow": 1,
    "next day": 2,
}

def get_date_from_sentence(sentence):
    # Lowercase the sentence to ensure we catch all instances
    sentence = sentence.lower()

    # Check for special cases
    for case in SPECIAL_CASES:
        if case in sentence:
            target_date = datetime.datetime.now() + datetime.timedelta(days=SPECIAL_CASES[case])
            return target_date.strftime(f"The date for {case} is %d/%m/%Y.")

    # Parse the day of the week from the sentence
    match = re.search(r"next (\w+)", sentence)
    if match:
        day_name = match.group(1)
    else:
        return "Couldn't find a day of the week in the sentence."

    # Check if the parsed day name is valid
    if day_name not in WEEKDAY_MAPPING:
        return "Invalid day of the week."

    # Get the current date
    now = datetime.datetime.now()

    # Get the weekday constant from the mapping
    weekday_constant = WEEKDAY_MAPPING[day_name]

    # Use dateutil's relativedelta to find the next specified day of the week
    next_day = now + relativedelta.re(weekday=weekday_constant)

    # Format the date as DD/MM/YYYY
    formatted_date = next_day.strftime("%d/%m/%Y")

    return f"The next {day_name.capitalize()} will be on {formatted_date}."

def detect_day1(sentence):
    # Lowercase the sentence to ensure we catch all instances
    sentence = sentence.lower()

    if "today" in sentence:
        return get_date("today")
    elif "tomorrow" in sentence:
        return get_date("tomorrow")
    elif "next day" in sentence:
        return get_date("next day")
    else:
        return get_date("today")