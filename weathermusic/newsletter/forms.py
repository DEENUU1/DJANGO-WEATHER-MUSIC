from django.forms import ModelForm
from .models import UserInfo
from django import forms


# This form works with UserInfo model and allows user to register for newsletter

class RegisterForm(ModelForm):

    class Meta:
        model = UserInfo
        fields = ('email', 'name', 'localization')


# This form allows to delete user from newsletter

class DeleteForm(forms.Form):
    email = forms.EmailField()
