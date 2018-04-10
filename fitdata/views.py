from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from oauth2.views import GetFitbitData
from fitbiters.models import Fitbiter
from fitdata.models import FitData

import datetime

def UpdateFitbitDataFunc():
	fitbiters=Fitbiter.objects.all()
	for fitbiter in fitbiters:
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
		

		#I'm cheating by hardcoding everything, also very inefficient
		#This is a stupid temporary hack		
		fitbiters=Fitbiter.objects.all()
		i=0
		fitbiter_data=[]
		for fitbiter in fitbiters:
			fitbiter_data.append(FitData.objects.filter(fitbiter=fitbiter).values_list('distance', flat=True).order_by('-date')[:5])
			i += 1
		
		five_latest_dates=FitData.objects.filter(fitbiter=fitbiter).values_list('date', flat=True).order_by('-date')[:5]
		all_data=[]
		for i in range(0,5):
			all_data.append([five_latest_dates[i],fitbiter_data[0][i],fitbiter_data[1][i]])

		context['all_data']=all_data
		context['fitbiters'] = fitbiters
		context['fitbiter_data']=fitbiter_data
		context['5_latest_dates']=FitData.objects.filter(fitbiter=fitbiter).values_list('date', flat=True).order_by('-date')[:5]
		return context