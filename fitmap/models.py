from django.db import models
from fitbiters.models import Fitbiter
from fitdata.models import FitData

class FitRoute(models.Model):
	title=models.CharField(max_length=100)
	start_lat=models.DecimalField(max_digits=10, decimal_places=6)
	start_long=models.DecimalField(max_digits=10, decimal_places=6)
	end_lat=models.DecimalField(max_digits=10, decimal_places=6)
	end_long=models.DecimalField(max_digits=10, decimal_places=6)
		
	def __str__(self):
		return '%s' %self.title

class FitMappedRte(models.Model):
	fitbiter=models.ForeignKey(Fitbiter, on_delete=models.PROTECT)
	fitroute=models.ForeignKey(FitRoute, on_delete=models.CASCADE)
	date=models.DateField()
	maprtedata=models.TextField()
	colour=models.CharField(max_length=7)
	order=models.PositiveSmallIntegerField();
	
	def __str__(self):
		return '%s on %s for %s' %(self.fitroute.title, self.date, self.fitbiter.fitbit_id)
	
	