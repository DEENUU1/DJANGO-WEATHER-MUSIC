from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from .news import News
from .views import news_list


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


class TestView(TestCase):

    def setUp(self) -> None:
        self.request = MagicMock()

    @patch('news.views.News')
    def test_news_list_view(self, mock_news_class):
        mock_news = MagicMock()
        mock_news.get_news.return_value = [
            MagicMock(
                title='UFO NAD USA',
                url='bestnews.com',
                image='image.png'
            ),
            MagicMock(
                title='BEST NEWS TODAY',
                url='bestnews.pl',
                image='photo.png'
            )
        ]

        mock_news_class.return_value = mock_news
        response = self.client.get(reverse('news:news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_list.html')
        self.assertEqual(len(response.context["news_articles"]), 2)
        self.assertEqual(response.context["news_articles"][0].title, 'UFO NAD USA')
        self.assertEqual(response.context["news_articles"][0].url, 'bestnews.com')
        self.assertEqual(response.context["news_articles"][0].image, 'image.png')
        self.assertEqual(response.context["news_articles"][1].title, 'BEST NEWS TODAY')
        self.assertEqual(response.context["news_articles"][1].url, 'bestnews.pl')
        self.assertEqual(response.context["news_articles"][1].image, 'photo.png')

