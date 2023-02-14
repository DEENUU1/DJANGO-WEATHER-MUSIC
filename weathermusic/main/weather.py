import os
from dataclasses import dataclass
import json
from requests import get
from dotenv import load_dotenv

load_dotenv()


@dataclass
class WeatherInfo:
    temp: int
    desc: str
    icon: str
    temp: float
    feels_like: float
    max_temp: float
    min_temp: float
    wind_speed: float


class Weather:
    """ This class allows to work with OpenWeatherMap API to return weather data
        based on the user localization """

    def __init__(self):
        self.api_key = os.getenv('WEATHER_KEY')

    def get_weather(self, localization: str):
        base_url = f'http://api.openweathermap.org/data/2.5/weather?appid=' \
                   f'{self.api_key}&q=' \
                   f'{localization}&units=metric&lang=en'
        result = get(base_url)
        json_result = json.loads(result.content)

        if result.status_code == 200:
            weather_temp = json_result['main']['temp']
            weather_feels = json_result['main']['feels_like']
            weather_max = json_result['main']['temp_max']
            weather_min = json_result['main']['temp_min']
            wind_speed = json_result['wind']['speed']
            weather_desc = json_result['weather'][0]['description']
            weather_icon = json_result['weather'][0]['icon']

            return WeatherInfo(
                temp=weather_temp,
                feels_like=weather_feels,
                max_temp=weather_max,
                min_temp=weather_min,
                wind_speed=wind_speed,
                desc=weather_desc,
                icon=weather_icon,

            )
        raise Exception("Nie działa")
