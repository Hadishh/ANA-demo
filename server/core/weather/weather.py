from bs4 import BeautifulSoup
import requests

from core.utils import (
    detect_day,
    detect_time,
    detect_locations_spacy,
    get_current_location,
    detect_locations_geotext,
)


class Weather:
    def __init__(self) -> None:
        pass

    def __weather(self, city, time, day):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        city = city.replace(" ", "+")
        res = requests.get(
            f"https://www.google.com/search?q={city}+weather+{time}+{day}&oq={city}+weather+{time}+{day}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8&hl=en",
            headers=headers,
        )
        soup = BeautifulSoup(res.text, "html.parser")
        location = soup.select("#wob_loc")[0].getText().strip()
        time1 = soup.select("#wob_dts")[0].getText().strip()
        info = soup.select("#wob_dc")[0].getText().strip()
        weather = soup.select("#wob_tm")[0].getText().strip()
        precipitation = soup.select("#wob_pp")[0].getText().strip()
        humidity = soup.select("#wob_hm")[0].getText().strip()
        weather = weather + "C"
        return (
            "day: "
            + day
            + ", time: "
            + time
            + ", Location: "
            + city
            + ", weather: "
            + info
            + ", temperature: "
            + weather
            + ", precipitation: "
            + precipitation
            + ", humidity: "
            + humidity
        )

    def get_weather(self, input):
        if detect_day(input):
            day = detect_day(input)
        else:
            day = "today"
        if detect_time(input):
            time = detect_time(input)
        else:
            time = ""

        if detect_locations_spacy(input):
            city = detect_locations_spacy(input)
        elif detect_locations_geotext(input):
            city = detect_locations_geotext(input)
        else:
            city = get_current_location()

        city = "".join(city)
        return self.__weather(city, time, day)

    def get_weather_by_city(self, city, day, time=""):
        return self.__weather(city, time, day)
