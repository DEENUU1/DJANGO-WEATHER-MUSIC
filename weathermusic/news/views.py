from django.shortcuts import render
from .news import News


def news_list(request):
    news = News()
    news_articles = news.get_news(request)

    context = {
        "news_articles": news_articles,
    }

    return render(request,
                  'news_list.html',
                  context)
