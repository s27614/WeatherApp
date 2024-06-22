import os
from flask import Flask, render_template, request

from mongodb import store_weather_data
from weather import get_current_weather
from waitress import serve
from datetime import datetime
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['weather_app']
collection = db['weather_data']


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')



    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        # You could render "City Not Found" instead like we do below
        city = "Warsaw"

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    temperature = weather_data['main']['temp']
    weather_desc = weather_data['weather'][0]['description'].capitalize()
    feels_like = weather_data['main']['feels_like']

    icon_code = weather_data['weather'][0]['icon']

    weather_icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    local_time = weather_data.get('local_time', 'N/A')
    utc_time = weather_data.get('utc_time', 'N/A')



    store_weather_data(
        city=city,
        temperature=weather_data['main']['temp'],
        weather_desc=weather_data['weather'][0]['description'].capitalize(),
        feels_like=weather_data['main']['feels_like'],
        icon_code=weather_data['weather'][0]['icon'],
        local_time=local_time,
        utc_time=utc_time
    )




    return render_template(
        "weather.html",
        title=city.capitalize(),
        status=weather_desc,
        temp=f"{temperature:.1f}°C",
        feels_like=f"{feels_like:.1f}°C",
        local_time=local_time,
        utc_time=utc_time,
        weather_icon_url=weather_icon_url

    )




if __name__ == "__main__":
    serve(app, host="localhost", port=5000, debug=True)
