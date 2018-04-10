from django.db import models
from fitbiters.models import Fitbiter
from fitdata.models import FitData

class StartPoint(models.Model):
	name=models.CharField(max_length=25)
	lat=models.DecimalField(max_digits=10, decimal_places=6)
	long=models.DecimalField(max_digits=10, decimal_places=6)
	
	def __str__(self):
		return '%s' %self.name

class EndPoint(models.Model):
	name=models.CharField(max_length=25)
	lat=models.DecimalField(max_digits=10, decimal_places=6)
	long=models.DecimalField(max_digits=10, decimal_places=6)
	
	def __str__(self):
		return '%s' %self.name
			
class WayPoint(models.Model):
	name=models.CharField(max_length=25)
	lat=models.DecimalField(max_digits=10, decimal_places=6)
	long=models.DecimalField(max_digits=10, decimal_places=6)
	
	def __str__(self):
		return '%s' %self.name
		
class FitRoute(models.Model):
	name=models.CharField(max_length=25)
	start=models.ForeignKey(StartPoint, on_delete=models.CASCADE)
	end=models.ForeignKey(EndPoint, on_delete=models.CASCADE)
	waypoints=models.ManyToManyField(WayPoint)
		
	def __str__(self):
		return '%s' %self.name

class FitMappedRte(models.Model):
	fitbiter=models.ForeignKey(Fitbiter, on_delete=models.PROTECT)
	fitroute=models.ForeignKey(FitRoute, on_delete=models.CASCADE)
	date=models.DateField()
	maprtedata=models.TextField()
	colour=models.CharField(max_length=7)
	order=models.PositiveSmallIntegerField();
	
	def __str__(self):
		return '%s on %s' %(self.fitroute.name, self.date)
	
	