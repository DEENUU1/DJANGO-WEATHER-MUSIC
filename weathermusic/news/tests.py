import unittest
import json
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse

from .news import News
from .views import news_list


class TestUrls(SimpleTestCase):

    def test_main_url_resolve(self):
        url = reverse('news:news')
        self.assertEqual(resolve(url).func, news_list)


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
            )
        ]

        mock_news_class.return_value = mock_news
        response = self.client.get(reverse('news:news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_list.html')
        self.assertEqual(len(response.context["news_articles"]), 1)
        self.assertEqual(response.context["news_articles"][0].title, 'UFO NAD USA')
        self.assertEqual(response.context["news_articles"][0].url, 'bestnews.com')
        self.assertEqual(response.context["news_articles"][0].image, 'image.png')


class TestNews(unittest.TestCase):

    @patch('news.news.get')
    def test_get_news(self, mock_get):
        json_data = {'articles': [{'title': 'Article 1', 'url': 'https://test.com/1', 'urlToImage': ''},
                                  {'title': 'Article 2', 'url': 'https://test.com/2', 'urlToImage': None}]}

        self.api_key = 'testtest123'
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(json_data).encode('utf-8')
        mock_get.return_value = mock_response

        mock_request = MagicMock()
        result = News.get_news(self, mock_request)

        self.assertEqual(result[0].title, 'Article 1')
        self.assertEqual(result[0].url, 'https://test.com/1')
        self.assertEqual(result[0].image, '')

        self.assertEqual(result[1].title, 'Article 2')
        self.assertEqual(result[1].url, 'https://test.com/2')
        self.assertEqual(result[1].image, None)

