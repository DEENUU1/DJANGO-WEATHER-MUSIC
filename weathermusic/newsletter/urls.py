from django.urls import path
from . import views


app_name = 'newsletter'


urlpatterns = [
    path('', views.register_view, name='register'),
    path('delete/', views.delete_view, name='delete')
]