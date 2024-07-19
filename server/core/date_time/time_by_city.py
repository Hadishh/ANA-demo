from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz


def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="city_time_locator")
    location = geolocator.geocode(city_name)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def get_city_timezone(lat, lon):
    tf = TimezoneFinder()
    return tf.timezone_at(lng=lon, lat=lat)


def get_city_time(city_name):
    lat, lon = get_city_coordinates(city_name)

    if lat is not None and lon is not None:
        timezone_str = get_city_timezone(lat, lon)

        if timezone_str:
            city_timezone = pytz.timezone(timezone_str)
            city_time = datetime.now(city_timezone)
            city_time = city_time.strftime("%Y-%m-%d %H:%M:%S")
            return f"Current time in {city_name}: {city_time}"
        else:
            return "Timezone could not be determined for this city."
    else:
        return "City not found."


if __name__ == "__main__":
    # Example usage
    city = "edmonton"  # This can be any city name
    current_time = get_city_time(city)
    print(f"Current time in {city}: {current_time}")
