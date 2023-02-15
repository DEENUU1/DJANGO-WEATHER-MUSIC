from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from .models import UserInfo


# subject, list of receivers and message to send a newsletter

class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Content")


# Getting user's data to register user to newsletter

class RegisterForm(ModelForm):

    class Meta:
        model = UserInfo
        fields = ('email', 'name', 'localization')


# Form to delete user from newsletter

class DeleteForm(forms.Form):
    email = forms.EmailField()
