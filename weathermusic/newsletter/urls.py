from django.urls import path
from . import views


app_name = 'newsletter'


urlpatterns = [
    path('', views.newsletter_view, name='newsletter')
]