from django.urls import path
from . import views


app_name = 'spotify_api'


urlpatterns = [
    path('', views.main_view, name='spotify')
]