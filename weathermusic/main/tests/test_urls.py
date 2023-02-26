from django.test import SimpleTestCase
from django.urls import resolve, reverse
from main.views import main_view


class TestUrls(SimpleTestCase):
    """ Tests Cases for urls in Django"""
    def test_main_url_resolve(self):
        """ Test for the main url """
        url = reverse('weather_music:main')
        self.assertEqual(resolve(url).func, main_view)
