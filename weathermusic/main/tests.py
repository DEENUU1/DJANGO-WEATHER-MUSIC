import datetime
import unittest
import json
import responses
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from .localization import Geolocation
from .spotify import SpotifyCategory, SpotifyAccess
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
            'playlist_url': 'https://londoncloudy.com',
        }
        # mock to return user local time
        mock_datetime.now.return_value = datetime.datetime(2023, 2, 11, 11, 0)

        response = self.client.get(reverse('weather_music:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


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


class TestWeather(unittest.TestCase):

    @patch('main.weather.get')
    def test_get_weather(self, mock_get):
        json_data = {'main': {'temp': 20, 'feels_like': 18, 'temp_min': 15, 'temp_max': 25},
                     'wind': {'speed': 5}, 'weather': [{'description': 'sunny', 'icon': '01d'}]}

        mock_result = MagicMock()
        mock_result.content = json.dumps(json_data).encode('utf=8')
        mock_result.status_code = 200
        mock_get.return_value = mock_result

        result = Weather().get_weather('Poland')
        self.assertEqual(result.temp, 20)
        self.assertEqual(result.desc, 'sunny')
        self.assertNotEqual(result.feels_like, '20')


class TestSpotify(unittest.TestCase, SpotifyAccess):

    @responses.activate
    def test_search_playlist_success(self):
        responses.get(
            url=f"https://api.spotify.com/v1/playlists/6afj5vDI8wGVNrUlRoSsg2",
            json={'external_urls': {'spotify': 'https://testplaylisturl.com'}},
            status=200,
        )

        self.assertEqual(SpotifyCategory._search_playlist(self,'test', '6afj5vDI8wGVNrUlRoSsg2'),
                         'https://testplaylisturl.com')
