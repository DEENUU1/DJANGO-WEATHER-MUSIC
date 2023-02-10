from django.shortcuts import render
from .spotify import SpotifyCategory, SpotifyAccess
from django.contrib import messages
from .weather import Weather
from .localization import Geolocation


def main_view(request):
    """ Main view that is displayed on the website. It uses functions below
        to easily get information from the API"""

    city_name = get_city_name(request)
    weather_info = get_weather_info(city_name, request)
    playlist_info = get_playlist_info(weather_info)

    context = {
        'playlist_title': playlist_info['playlist_title'],
        'playlist_url': playlist_info['playlist_url'],
        'playlist_image': playlist_info['playlist_image'],
        'weather_city': city_name,
        'weather_temp': weather_info.temp,
        'weather_desc': weather_info.desc,
        'weather_icon': weather_info.icon,
        "weather_feels": weather_info.feels_like,
        "weather_max": weather_info.max_temp,
        "weather_min": weather_info.min_temp,
        "wind_speed": weather_info.wind_speed,
    }

    return render(request,
                  'index.html',
                  context)


def get_city_name(request):
    """ This function allows to get geolocation by ip address or from HTML form"""

    geolocation = Geolocation()
    ip_address = geolocation.get_ipaddress(request)

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

    playlist_title, playlist_url, playlist_image = spotify_func.random_playlist(token, weather_info.desc)

    return {
        'playlist_title': playlist_title,
        'playlist_url': playlist_url,
        'playlist_image': playlist_image
    }
