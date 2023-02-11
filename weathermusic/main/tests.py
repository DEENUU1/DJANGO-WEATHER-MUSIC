from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from .views import main_view
from unittest.mock import MagicMock, patch
import datetime


class TestUrls(SimpleTestCase):

    def test_main_resolve(self):
        url = reverse('weather_music:main')
        self.assertEqual(resolve(url).func, main_view)


class MainViewTests(TestCase):

    @patch('main.views.get_city_name')
    @patch('main.views.get_weather_info')
    @patch('main.views.get_playlist_info')
    @patch('main.views.News')
    @patch('main.views.datetime')
    def test_main_view(self, mock_datetime, mock_news, mock_playlist_info, mock_weather_info, mock_city_name):
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
        mock_playlist_info.return_value = {
            'playlist_title': 'London Cloudy Playlist',
            'playlist_url': 'https://londoncloudy.com',
            'playlist_image': 'cloudy.jpg'
        }
        mock_news.return_value = MagicMock(
            get_news=MagicMock(return_value=[{
                'title': 'News article 1',
                'url': 'https://news.com/1',
                'img_url': 'news1.jpg'
            }, {
                'title': 'News article 2',
                'url': 'https://news.com/2',
                'img_url': 'news2.jpg'
            }])
        )
        mock_datetime.now.return_value = datetime.datetime(2023, 2, 11, 11, 0)

        response = self.client.get(reverse('weather_music:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.context['playlist_title'], 'London Cloudy Playlist')

