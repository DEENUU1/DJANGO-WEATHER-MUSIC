from django.db import models
from django.utils import timezone


# This model allows to create model form
# To get user contact information for sending daily newsletter
# date is added automatically, user have to send email, name and localization

class UserInfo(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=20)
    localization = models.CharField(max_length=20)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
