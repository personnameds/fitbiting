from django.db import models
from runners.models import Runner
		
class Route(models.Model):
	title=models.CharField(max_length=100)
	start_lat=models.DecimalField(max_digits=10, decimal_places=6)
	start_long=models.DecimalField(max_digits=10, decimal_places=6)
	end_lat=models.DecimalField(max_digits=10, decimal_places=6)
	end_long=models.DecimalField(max_digits=10, decimal_places=6)
	finished=models.BooleanField(default=False, blank=True)
	start_date=models.DateField()
	
	def __str__(self):
		return '%s' %self.title

##RteRunners are Runners who are attached to this route
class RteRunner(models.Model):
	route=models.ForeignKey(Route, on_delete=models.CASCADE)
	runner=models.ForeignKey(Runner, on_delete=models.CASCADE)
	colour=models.CharField(max_length=7)
	
	def __str__(self):
		return 'RteRunner %s in %s' %(self.runner, self.route)