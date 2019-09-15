from django.db import models
from fitbiters.models import Fitbiter
from fitdata.models import FitData
		
class FitRoute(models.Model):
	title=models.CharField(max_length=100)
	start_lat=models.DecimalField(max_digits=10, decimal_places=6)
	start_long=models.DecimalField(max_digits=10, decimal_places=6)
	end_lat=models.DecimalField(max_digits=10, decimal_places=6)
	end_long=models.DecimalField(max_digits=10, decimal_places=6)
	finished=models.BooleanField(default=False, blank=True)
	start_date=models.DateField()
	
	def __str__(self):
		return '%s' %self.title

##Fitrunners are Fitbiters who are attached to this route
class FitRunner(models.Model):
	fitroute=models.ForeignKey(FitRoute, on_delete=models.CASCADE)
	fitbiter=models.ForeignKey(Fitbiter, on_delete=models.CASCADE)
	colour=models.CharField(max_length=7)
	
	def __str__(self):
		return '%s in %s' %(self.fitbiter.fitbit_id, self.fitroute)