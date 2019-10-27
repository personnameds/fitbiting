from django.db import models

class Platform(models.Model):
	name=models.CharField(max_length=10)
	client_id=models.CharField(max_length=10,default='')
	client_secret=models.CharField(max_length=50,default='')
	redirect_uri=models.CharField(max_length=100,default='')
	
	def __str__(self):
		return '%s' %self.name
	
