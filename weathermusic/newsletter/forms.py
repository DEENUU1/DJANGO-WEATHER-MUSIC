from django.forms import ModelForm
from .models import UserInfo
from django import forms
from tinymce.widgets import TinyMCE


# This form allows admin user to create email content

class NewsletterForm(forms.Form):
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Content")


# This form works with UserInfo model and allows user to register for newsletter

class RegisterForm(ModelForm):

    class Meta:
        model = UserInfo
        fields = ('email', 'name', 'localization')


# This form allows to delete user from newsletter

class DeleteForm(forms.Form):
    email = forms.EmailField()
