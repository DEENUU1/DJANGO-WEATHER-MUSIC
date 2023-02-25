import datetime
import unittest
import json
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from .localization import Geolocation
from .spotify import SpotifyCategory
from .views import main_view
from .weather import Weather


class TestUrls(SimpleTestCase):

    def test_main_url_resolve(self):
        url = reverse('weather_music:main')
        self.assertEqual(resolve(url).func, main_view)


class MainViewTests(TestCase):

    @patch('main.views.get_city_name')
    @patch('main.views.get_weather_info')
    @patch('main.views.get_playlist_info')
    @patch('main.views.datetime')
    def test_main_view(self, mock_datetime, mock_playlist_info, mock_weather_info, mock_city_name):
        # mock to return city name
        mock_city_name.return_value = 'London'
        # mock to return weather data
        mock_weather_info.return_value = MagicMock(
            temp=10,
            desc='cloudy',
            icon='cloudy.png',
            feels_like=8,
            max_temp=12,
            min_temp=5,
            wind_speed=5
        )
        # mock to return spotify playlist info
        mock_playlist_info.return_value = {
            'playlist_title': 'London Cloudy Playlist',
            'playlist_url': 'https://londoncloudy.com',
            'playlist_image': 'cloudy.jpg'
        }
        # mock to return user local time
        mock_datetime.now.return_value = datetime.datetime(2023, 2, 11, 11, 0)

        response = self.client.get(reverse('weather_music:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['playlist_title'], 'London Cloudy Playlist')

class TestLocalization(unittest.TestCase):

    @patch('main.localization.Geolocation._get_ipAddress_information')
    def test_return_localization_success(self, mock_get_information):
        mock_get_information.return_value = {'city': 'Warsaw'}
        self.assertEqual(Geolocation().return_location('192.168.0.1'), 'Warsaw')

    @patch('main.localization.Geolocation._get_ipAddress_information')
    def test_return_country_code(self, mock_get_country_code):
        mock_get_country_code.return_value = {'country_code': 'PL'}
        self.assertEqual(Geolocation().return_country_code('192.168.0.1'), 'PL')

    def test_get_ipAddress_information(self):
        json_data = {'city': 'Lodz', 'country_code': 'PL'}
        mock_result = MagicMock()
        mock_result.content = json.dumps(json_data).encode('utf-8')

        with patch('main.localization.get', return_value=mock_result):
            result = Geolocation()._get_ipAddress_information('192.168.0.1')
            self.assertEqual(result, json_data)





class TestWeather(TestCase):

    def setUp(self) -> None:
        self.localization = "Poland"

    @patch('main.weather.Weather.get_weather')
    def test_return_weather_data(self, mock_get_weather):
        mock_get_weather.return_value = MagicMock(
            temp=10,
            desc='cloud',
            icon='cloud.png',
            feels_like=8,
            max_temp=12,
            min_temp=5,
            wind_speed=5
        )
        weather = Weather()
        weather_data = weather.get_weather(self.localization)
        self.assertEqual(weather_data.temp, 10)
        self.assertEqual(weather_data.desc, 'cloud')
        self.assertEqual(weather_data.icon, 'cloud.png')
        self.assertEqual(weather_data.feels_like, 8)
        self.assertEqual(weather_data.max_temp, 12)
        self.assertEqual(weather_data.min_temp, 5)
        self.assertEqual(weather_data.wind_speed, 5)







