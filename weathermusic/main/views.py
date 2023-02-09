
from django.shortcuts import render
from .spotify import SpotifyCategory, SpotifyAccess
from django.contrib import messages
from .weather import Weather
from .localization import Geolocation
from django.views import View


class MainView(View):

    @staticmethod
    def get_context(request):
        geolocation = Geolocation()
        ip_address = geolocation.get_ipaddress(request)
        city_name = geolocation.return_location(ip_address)
        spotify_access = SpotifyAccess()
        spotify_token = spotify_access._get_token()
        spotify_category = SpotifyCategory()
        weather = Weather()
        weather_info = weather.get_weather(city_name)

        context = {
            'playlist_title': "",
            'playlist_url': "",
            'playlist_image': "",
            'weather_city': city_name,
            'weather_temp': weather_info.temp if weather_info else "",
            'weather_desc': weather_info.desc if weather_info else "",
            'weather_icon': weather_info.icon if weather_info else "",
            "weather_feels": weather_info.feels_like if weather_info else "",
            "weather_max": weather_info.max_temp if weather_info else "",
            "weather_min": weather_info.min_temp if weather_info else "",
            "widn_speed": weather_info.wind_speed if weather_info else "",
        }

        try:
            playlist_title, playlist_url, playlist_image = spotify_category.random_playlist(spotify_token, weather_info.desc)

            context.update({
                "playlist_title": playlist_title,
                "playlist_url": playlist_url,
                "playlist_image": playlist_image
            })

        except TypeError:
            messages.error(request, "Podaj poprawną lokalizację")
        except ValueError:
            messages.error(request, 'Podaj poprawną lokalizację')
        return context

    def get(self, request):
        context = self.get_context(request)
        return render(request, "index.html", context)
