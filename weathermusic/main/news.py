from requests import get
import json
from dotenv import load_dotenv
import os
from dataclasses import dataclass
from .localization import Geolocation

load_dotenv()


@dataclass()
class NewsInfo:
    title: str
    url: str
    image: str


class News:
    """ This class allows to return news based on user localization """

    def __init__(self):
        self.api_key = os.getenv('NEWS_KEY')

    def get_news(self, request):
        geolocation = Geolocation()
        ip_address = geolocation.get_ipaddress(request)
        country_code = geolocation.return_country_code(ip_address)

        base_url = f'https://newsapi.org/v2/top-headlines?country={country_code}&apiKey={self.api_key}'
        result = get(base_url)
        json_result = json.loads(result.content)
        articles = json_result['articles']

        if result.status_code == 200:
            all_articles = []
            for article in articles:
                article_title = article['title']
                article_url = article['url']
                article_image = article['urlToImage']

                all_articles.append(NewsInfo(
                    title=article_title,
                    url=article_url,
                    image=article_image,
                ))
            return all_articles
        else:
            raise Exception("Nie działa")

