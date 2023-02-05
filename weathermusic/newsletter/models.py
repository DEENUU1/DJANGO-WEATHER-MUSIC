from django.db import models


# This model allows to create model form
# To get user contact information for sending daily newsletter

class UserInfo(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=20)
    localization = models.CharField(max_length=20)

    def __str__(self):
        return self.localization
