from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from oauth2.views import GetFitbitData
from fitbiters.models import Fitbiter
from fitdata.models import FitData
from fitdata.forms import FitDataForm
from fitmap.models import FitRoute, FitMappedRte

import datetime

##Form that asks what data should be displayed
class FitDataIndexView(FormView):
	template_name='fitdata/fitdata_form.html'
	form_class=FitDataForm
	
	def form_valid(self, form):
		self.form = form
		return HttpResponseRedirect(self.get_success_url())
		
	def get_success_url(self):
		if self.form.cleaned_data['all_fitbiters']:
			return reverse('fitdata-display', kwargs={'data_type':'fitbiters', 'ids':'all'})
		elif self.form.cleaned_data['fitbiters']:
			fitbiters=",".join(str(f.id) for f in self.form.cleaned_data['fitbiters'])
			return reverse('fitdata-display', kwargs={'data_type':'fitbiters', 'ids':fitbiters})
		elif self.form.cleaned_data['routes']:
			route_id=self.form.cleaned_data['routes'].id
			return reverse('fitdata-display', kwargs={'data_type':'route', 'ids':route_id})
		
##Downloads data from Fitbit
##Also updates keys etc.	
def UpdateFitbitDataFunc(fitbiters):
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

class FitDataDisplayView(TemplateView):
	template_name="fitdata/fitdata_display.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		##Retrieves what data needs to be displayed based on Form from FitDataIndex
		data_type=kwargs['data_type']
		ids=kwargs['ids']
		
		if data_type=='fitbiters':
			if ids=='all':
				fitbiters=Fitbiter.objects.all()
			else:
				ids=ids.split(',')
				fitbiters=Fitbiter.objects.filter(pk__in=ids)
		elif data_type=='route':
			fitroute=FitRoute.objects.get(pk__in=ids)
			ids=FitMappedRte.objects.filter(fitroute=fitroute).values_list('fitbiter', flat=True)
			fitbiters=Fitbiter.objects.filter(pk__in=ids)
		
		##Based on data displays calls the UpdateFitbitData Function
		UpdateFitbitDataFunc(fitbiters)
		
		##Works up to here
		five_latest_dates=[]##[datetime.datetime.today()]		
		for i in range(5,-1,-1):
			five_latest_dates.append(datetime.datetime.today()-datetime.timedelta(days=i))
		
		all_data=[]
		for date in five_latest_dates:
			fitbiter_data=[date.date()]
			for fitbiter in fitbiters:
				fitbiter_data.append(FitData.objects.get(fitbiter=fitbiter, date=date).distance)
			all_data.append(fitbiter_data)

		context['all_data']=all_data
		context['fitbiters'] = fitbiters
		return context