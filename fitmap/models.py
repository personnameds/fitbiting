from django.db import models
from fitbiters.models import Fitbiter
from fitdata.models import FitData
		
class FitRoute(models.Model):
	title=models.CharField(max_length=100)
	start_lat=models.DecimalField(max_digits=10, decimal_places=6)
	start_long=models.DecimalField(max_digits=10, decimal_places=6)
	end_lat=models.DecimalField(max_digits=10, decimal_places=6)
	end_long=models.DecimalField(max_digits=10, decimal_places=6)
	last_update=models.DateField()

	def __str__(self):
		return '%s' %self.title

##Fitrunners are Fitbiters who are attached to this route
class FitRunner(models.Model):
	fitroute=models.ForeignKey(FitRoute, on_delete=models.CASCADE)
	fitbiter=models.ForeignKey(Fitbiter, on_delete=models.CASCADE)
	colour=models.CharField(max_length=7)
	
	def __str__(self):
		return '%s' %self.fitbiter.fitbit_id

class FitMappedRte(models.Model):
	fitrunner=models.ForeignKey(FitRunner, on_delete=models.CASCADE)
	fitroute=models.ForeignKey(FitRoute, on_delete=models.CASCADE)
	date=models.DateField()
	maprtedata=models.TextField() 
	order=models.PositiveSmallIntegerField();
	
	def __str__(self):
		return '%s on %s for %s' %(self.fitroute.title, self.date, self.fitrunner.fitbiter.fitbit_id)
	
	