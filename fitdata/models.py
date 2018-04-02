from django.db import models

from fitbiters.models import Fitbiter

class FitData(models.Model):
	fitbiter=models.ForeignKey(Fitbiter, on_delete=models.CASCADE)
	date=models.DateField()
	distance=models.DecimalField(max_digits=10, decimal_places=2)
	
	class Meta:
		verbose_name='Fitbit Data'
		verbose_name_plural='Fitbit Data'
	
	def __str__(self):
		return '%s' %self.fitbiter
