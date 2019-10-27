from django.db import models
from runners.models import Runner

class RunData(models.Model):
	runner=models.ForeignKey(Runner, on_delete=models.CASCADE)
	date=models.DateField()
	distance=models.DecimalField(max_digits=10, decimal_places=2)
	
	class Meta:
		verbose_name='Run Data'
		verbose_name_plural='Run Data'
	
	def __str__(self):
		return 'Rundata %s' %self.runner
