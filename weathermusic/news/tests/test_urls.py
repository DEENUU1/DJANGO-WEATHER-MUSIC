from django.test import SimpleTestCase
from django.urls import resolve, reverse

from news.views import news_list


class TestUrls(SimpleTestCase):

    def test_main_url_resolve(self):
        url = reverse('news:news')
        self.assertEqual(resolve(url).func, news_list)
