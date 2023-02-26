import datetime
from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse


class MainViewTests(TestCase):
    """ Tests Cases for views in Django """
    @patch('main.views.get_city_name')
    @patch('main.views.get_weather_info')
    @patch('main.views.get_playlist_info')
    @patch('main.views.datetime')
    def test_main_view(self, mock_datetime, mock_playlist_info, mock_weather_info, mock_city_name):
        """ Test for the main view """
        mock_city_name.return_value = 'London'
        mock_weather_info.return_value = MagicMock(
            temp=10,
            desc='cloudy',
            icon='cloudy.png',
            feels_like=8,
            max_temp=12,
            min_temp=5,
            wind_speed=5
        )
        mock_playlist_info.return_value = {'playlist_url': 'https://londoncloudy.com'}
        mock_datetime.now.return_value = datetime.datetime(2023, 2, 11, 11, 0)
        response = self.client.get(reverse('weather_music:main'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
