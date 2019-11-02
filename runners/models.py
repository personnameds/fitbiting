from django.db import models

from django.contrib.auth.models import User
from oauth2.models import Platform

class Runner(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	goal=models.DecimalField(max_digits=6, decimal_places=2)
	goal_set_date=models.DateField()
	platform=models.ForeignKey(Platform, on_delete=models.PROTECT)
	
	def __str__(self):
		return 'Runner %s %s' %(self.user, self.platform) 
	
	
class Fitbiter(models.Model):
    runner=models.OneToOneField(Runner, on_delete=models.CASCADE)
    fitbit_id=models.CharField(max_length=15, unique=True)
    access_token=models.CharField(max_length=255)
    refresh_token=models.CharField(max_length=255)

    def __str__(self):
        return 'Fitbiter %s' %self.fitbit_id 

class Stravaer(models.Model):
    runner=models.OneToOneField(Runner, on_delete=models.CASCADE)
    strava_id=models.CharField(max_length=15, unique=True)
    access_token=models.CharField(max_length=255)
    refresh_token=models.CharField(max_length=255)

    def __str__(self):
        return 'Stavaer %s' %self.strava_id 