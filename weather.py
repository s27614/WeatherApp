from datetime import datetime
from dotenv import load_dotenv
from pprint import pprint
import requests
import os
import pytz
from pymongo import MongoClient

from mongodb import store_weather_data

load_dotenv()
client = MongoClient('mongodb://localhost:27017/')
db = client['weather_app']
collection = db['weather_data']


def get_current_weather(city="Warsaw"):

    request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=metric'

    weather_data = requests.get(request_url).json()

    print(weather_data)

    if weather_data.get('cod') == '404':
        return {'cod': 404, 'message': 'City not found'}
    elif weather_data.get('cod') != 200:
        return {'cod': weather_data.get('cod', 'unknown'), 'message': weather_data.get('message', 'Unknown error')}





    if weather_data['cod'] == 200:
        # Get local time
        timezone_str = weather_data['timezone']
        try:
            country_code = weather_data['sys']['country']
            timezones = pytz.country_timezones.get(country_code, [])
            if timezones:
                timezone = pytz.timezone(timezones[0])  # Use the first timezone if multiple
            else:
                timezone = pytz.timezone('UTC')  # Default to UTC if no timezones found
        except (KeyError, pytz.exceptions.UnknownTimeZoneError) as e:
            print(f"Error fetching timezone: {e}")
            timezone = pytz.timezone('UTC')

        utc_now = datetime.now(pytz.utc)
        local_time = utc_now.astimezone(timezone).strftime("%d %b %Y | %I:%M:%S %p")



        # Add local time to weather data
        weather_data['local_time'] = local_time

        # Get UTC time
        utc_time = utc_now.strftime("%d %b %Y | %I:%M:%S %p")
        weather_data['utc_time'] = utc_time





    return weather_data


if __name__ == "__main__":
    print('\n*** Get Current Weather Conditions ***\n')
    city = input("\nPlease enter a city name: ")
    weather_data = get_current_weather(city)

    print("\n")
    pprint(weather_data)