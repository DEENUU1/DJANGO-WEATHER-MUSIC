from django.shortcuts import render
from . import spotify, weather, playlists
from django.contrib import messages
from random import choice


def main_view(request):

    # Spotify API configuration
    token = spotify.get_token()

    # Weather API configuration

    playlist_title = ""
    playlist_url = ""
    playlist_image = ""
    weather_temp = ""
    weather_desc = ""
    weather_icon = ""

    city_name = None
    if request.method == 'POST':
        city_name = request.POST['city']
        try:
            weather.get_weather(city_name)
            weather_temp, weather_desc, weather_icon = weather.get_weather(city_name)

            for weather_key in playlists.WEATHER_PLAYLISTS.keys():
                if weather_key in weather_desc:
                    playlist_id = choice(playlists.WEATHER_PLAYLISTS[weather_key])[1]
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
    }

    return render(request, 'index.html',
                  context)