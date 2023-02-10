from requests import get
import json
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import datetime

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

    def get_news(self):
        base_url = f'https://newsapi.org/v2/top-headlines?country=pl&apiKey={self.api_key}'
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

