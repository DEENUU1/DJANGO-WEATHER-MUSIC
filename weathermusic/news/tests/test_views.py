from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.urls import reverse


class TestView(TestCase):

    @patch('news.views.News')
    def test_news_list_view(self, mock_news_class):
        mock_news = MagicMock()
        mock_news.get_news.return_value = [
            MagicMock(
                title='UFO NAD USA',
                url='bestnews.com',
                image='image.png')]
        mock_news_class.return_value = mock_news
        response = self.client.get(reverse('news:news'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news_list.html')
        self.assertEqual(len(response.context["news_articles"]), 1)
        self.assertEqual(response.context["news_articles"][0].title, 'UFO NAD USA')
        self.assertEqual(response.context["news_articles"][0].url, 'bestnews.com')
        self.assertEqual(response.context["news_articles"][0].image, 'image.png')
