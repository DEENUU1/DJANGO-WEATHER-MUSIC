from django.shortcuts import render
from . import spotify, weather, playlists, localization
from django.contrib import messages
import random


def main_view(request):
    # geolocation
    ip_address = localization.get_ip(request)

    if request.method == 'POST':
        city_name = request.POST['city']
    else:
        city_name = localization.geolocation(ip_address)

    # Spotify API configuration
    token = spotify.get_token()

    # Weather API configuration

    playlist_title = ""
    playlist_url = ""
    playlist_image = ""
    weather_temp = ""
    weather_desc = ""
    weather_icon = ""
    weather_feels = ""
    weather_max = ""
    weather_min = ""
    wind_speed = ""

    if city_name:
        try:
            weather.get_weather(city_name)
            weather_temp, weather_desc, weather_icon, weather_min, weather_max, weather_feels, wind_speed = weather.get_weather(city_name)

            for weather_key in playlists.WEATHER_PLAYLISTS.keys():
                if weather_key in weather_desc:
                    playlist_id = random.choice(playlists.WEATHER_PLAYLISTS[weather_key])[1]
                    playlist_title, playlist_url, playlist_image = spotify.search_playlist(token, playlist_id)

        except TypeError:
            messages.error(request, 'Podaj poprawną lokalizację')
        except ValueError:
            messages.error(request, 'Podaj poprawną lokalizację')

    context = {
        'playlist_title': playlist_title,
        'playlist_url': playlist_url,
        'playlist_image': playlist_image,
        'weather_city': city_name,
        'weather_temp': weather_temp,
        'weather_desc': weather_desc,
        'weather_icon': weather_icon,
        "weather_feels": weather_feels,
        "weather_max": weather_max,
        "weather_min": weather_min,
        "wind_speed": wind_speed,
    }

    return render(request,
                  'index.html',
                  context)