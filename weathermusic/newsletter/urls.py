from django.urls import path
from . import views


app_name = 'newsletter'


urlpatterns = [
    path('', views.register_view, name='register'),
    path('success', views.success, name='success'),
    path('error', views.error, name='error')
]