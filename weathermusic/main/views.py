from datetime import datetime

from django.contrib import messages
from django.shortcuts import render

from .localization import Geolocation, IPScraper
from .spotify import SpotifyCategory, SpotifyAccess
from .weather import Weather


def main_view(request):
    """ Main view that is displayed on the website. It uses functions below
        to easily get information from the API"""

    city_name = get_city_name(request)
    weather_info = get_weather_info(city_name, request)
    playlist_info = get_playlist_info(weather_info)
    time = datetime.now()
    time_format = time.strftime("%H:%M")

    context = {
        'playlist_url': playlist_info['playlist_url'],
        'weather_city': city_name,
        'weather_temp': weather_info.temp,
        'weather_desc': weather_info.desc,
        'weather_icon': weather_info.icon,
        "weather_feels": weather_info.feels_like,
        "weather_max": weather_info.max_temp,
        "weather_min": weather_info.min_temp,
        "wind_speed": weather_info.wind_speed,
        "time": time_format,
    }

    return render(request,
                  'index.html',
                  context)


def get_city_name(request):
    """ This function allows to get geolocation by ip address or from HTML form"""

    geolocation = Geolocation()
    ip_scraper = IPScraper()
    ip_address = ip_scraper.get_ipaddress(request)

    if request.method == 'POST':
        city_name = request.POST['city']
    else:
        city_name = geolocation.return_location(ip_address)

    return city_name


def get_weather_info(city_name: str, request):
    """ This function return the weather info for specify city
        If city name is incorrect it will return message error"""

    try:
        weather = Weather()
        weather_info = weather.get_weather(city_name)
    except TypeError:
        messages.error(request, "Podaj poprawną lokalizację")
    except ValueError:
        messages.error(request, 'Podaj poprawną lokalizację')

    return weather_info


def get_playlist_info(weather_info: str):
    """ Based on the weather info it returns random playlist """

    spotify_api = SpotifyAccess()
    token = spotify_api._get_token()
    spotify_func = SpotifyCategory()

    playlist_url= spotify_func.get_random_playlist(token, weather_info.desc)

    return {
        'playlist_url': playlist_url,
    }