from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from oauth2.views import GetFitbitData
from fitbiters.models import Fitbiter
from fitdata.models import FitData

import datetime

def UpdateFitbitDataFunc(fitbiter):
	activity_data=GetFitbitData(fitbiter)
	distance_by_date=activity_data['activities-distance']
	for i in distance_by_date:
		fitdata=FitData(fitbiter=fitbiter,
				date=i['dateTime'],
				distance=i['value'],
				)
		fitdata.save()
	return;


class FitDataIndexView(TemplateView):
	template_name="fitdata/fitdataindex.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		fitbiters=Fitbiter.objects.all()
		for fitbiter in fitbiters:
			UpdateFitbitDataFunc(fitbiter)
		
		#context['fitbiters'] = fitbiters
		#context['5_latest_dates']=FitData.objects.values_list('date', flat=True).order_by('-date')[:5]
		return context