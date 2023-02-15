from django.urls import path

from .views import news_list

app_name = 'news'


urlpatterns = [
    path('', news_list, name='news')
]