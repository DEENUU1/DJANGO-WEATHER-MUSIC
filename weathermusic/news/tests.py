from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from unittest.mock import MagicMock, patch
from .views import news_list
from .news import NewsInfo, News


class TestUrls(SimpleTestCase):

    def test_main_url_resolve(self):
        url = reverse('news:news')
        self.assertEqual(resolve(url).func, news_list)


class TestNews(TestCase):

    def setUp(self) -> None:
        self.request = MagicMock()
        self.country_code = 'PL'

    @patch('news.news.News.get_news')
    def test_get_news(self, mock_get_news):
        mock_get_news.return_value = MagicMock(
            title='UFO NAD USA',
            url='bestnews.com',
            image='image.png',
        )
        news = News()
        news_data = news.get_news(self.request)

        self.assertEqual(news_data.title, 'UFO NAD USA')
        self.assertEqual(news_data.url, 'bestnews.com')
        self.assertEqual(news_data.image, 'image.png')


