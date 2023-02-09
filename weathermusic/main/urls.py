from django.urls import path
from .views import MainView


app_name = 'weather_music'


urlpatterns = [
    path('', MainView.as_view(), name='main')
]