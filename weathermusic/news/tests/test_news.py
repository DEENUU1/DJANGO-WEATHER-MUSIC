import unittest
import json
from unittest.mock import MagicMock, patch

from news.news import News


class TestNews(unittest.TestCase):
    """ Test Cases for news class methods """
    def setUp(self) -> None:
        with open('news/tests/news_fixture.json', encoding='utf-8') as json_file:
            self.fake_news_information = json.load(json_file)
        self.api_key = 'fakeapikey123'

    @patch('news.news.get')
    def test_get_news(self, mock_get):
        """ Test success get news from the API """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(self.fake_news_information)
        mock_get.return_value = mock_response
        mock_request = MagicMock()
        result = News.get_news(self, mock_request)

        self.assertEqual(result[0].title, 'Kiedy będzie ciepło? Wir polarny studzi nadzieje. "Nasz kawałek Europy przeniesie się w marcu w Arktykę". P... - TVN24')
        self.assertEqual(result[0].url, 'https://news.google.com/rss/articles/CBMipwFodHRwczovL3R2bjI0LnBsL3R2bm1ldGVvL3Byb2dub3phL2tpZWR5LWJlZHppZS1jaWVwbG8td2lyLXBvbGFybnktc3R1ZHppLW5hZHppZWplLW5hc3ota2F3YWxlay1ldXJvcHktcHJ6ZW5pZXNpZS1zaWUtdy1tYXJjdS13LWFya3R5a2UtcHJvZ25vemEtZGx1Z290ZXJtaW5vd2EtNjc3Nzk0NtIBqwFodHRwczovL2FtcC50dm4yNC5wbC90dm5tZXRlby9wcm9nbm96YS9raWVkeS1iZWR6aWUtY2llcGxvLXdpci1wb2xhcm55LXN0dWR6aS1uYWR6aWVqZS1uYXN6LWthd2FsZWstZXVyb3B5LXByemVuaWVzaWUtc2llLXctbWFyY3Utdy1hcmt0eWtlLXByb2dub3phLWRsdWdvdGVybWlub3dhLTY3Nzc5NDY?oc=5')
        self.assertEqual(result[0].image, None)

        self.assertEqual(result[1].title, 'Wojna w Ukrainie. Media: Rosjanie strzelali do siebie. Nawet pod Moskwą - wiadomosci.gazeta.pl')
        self.assertEqual(result[1].url, 'https://news.google.com/rss/articles/CBMieGh0dHBzOi8vd2lhZG9tb3NjaS5nYXpldGEucGwvd2lhZG9tb3NjaS83LDExNDg4MSwyOTUwMjE2NSx3b2puYS13LXVrcmFpbmllLW1lZGlhLXJvc2phbmllLXN0cnplbGFsaS1kby1zaWViaWUtbmF3ZXQuaHRtbNIBd2h0dHBzOi8vd2lhZG9tb3NjaS5nYXpldGEucGwvd2lhZG9tb3NjaS83LDExNDg4MSwyOTUwMjE2NSx3b2puYS13LXVrcmFpbmllLW1lZGlhLXJvc2phbmllLXN0cnplbGFsaS1kby1zaWViaWUtbmF3ZXQuYW1w?oc=5')
        self.assertEqual(result[1].image, None)

