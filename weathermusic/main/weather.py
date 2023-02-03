from requests import get
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('WEATHER_KEY')

# This function returns the basic weather information like
# description, temperature (in delicious) and icon


def get_weather(localization):
    base_url = f'http://api.openweathermap.org/data/2.5/weather?appid={API_KEY}&q={localization}&units=metric&lang=en'
    result = get(base_url)
    json_result = json.loads(result.content)

    if result.status_code == 200:
        weather_temp = json_result['main']['temp']
        weather_desc = json_result['weather'][0]['description']
        weather_icon = json_result['weather'][0]['icon']
        return weather_temp, weather_desc, weather_icon
    else:
        print('Nie działa')