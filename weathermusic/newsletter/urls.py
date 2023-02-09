from django.urls import path
from . import views
from .views import SignUpView, DeleteUserView, SendNewsletterView

app_name = 'newsletter'


urlpatterns = [
    path('', SignUpView.as_view(), name='register'),
    path('delete/', DeleteUserView.as_view(), name='delete'),
    path('send/', SendNewsletterView.as_view(), name='send'),
]