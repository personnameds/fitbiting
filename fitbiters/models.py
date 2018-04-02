from django.db import models

from django.contrib.auth.models import User

class Fitbiter(models.Model):
    #user=models.OneToOneField(User, on_delete=models.CASCADE)
    fitbit_id=models.CharField(max_length=15, unique=True)
    access_token=models.CharField(max_length=255)
    refresh_token=models.CharField(max_length=255)

    def __str__(self):
        return '%s' %self.fitbit_id 
