from django.urls import path
from . import views


app_name = 'weather_music'


urlpatterns = [
    path('', views.main_view, name='main')
]