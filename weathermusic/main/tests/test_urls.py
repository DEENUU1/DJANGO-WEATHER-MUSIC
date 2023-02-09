from django.test import SimpleTestCase
from django.urls import resolve, reverse
from main.views import MainView


class TestUrls(SimpleTestCase):

    def test_main_resolve(self):
        url = reverse('weather_music:main')
        self.assertEqual(resolve(url).func.view_class, MainView)