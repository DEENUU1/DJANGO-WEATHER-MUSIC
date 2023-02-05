from django.forms import ModelForm
from .models import UserInfo


# This form works with UserInfo model and allows user to register for newsletter

class NewsLetterForm(ModelForm):

    class Meta:
        model = UserInfo
        fields = ('email', 'name', 'localization')