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
		fitbiters = form.cleaned_data['fitbiters']
		fitbiter_ids=[]
		for fitbiter in fitbiters:
			fitbiter_ids.append(fitbiter.pk)
		self.fitbiter_ids=fitbiter_ids
		self.num_days=form.cleaned_data['num_days']
		return super().form_valid(form)
		
	def get_success_url(self):
		return reverse('fitdata-display', kwargs={'fitbiter_ids':self.fitbiter_ids,'num_days':self.num_days})
		
##Downloads data from Fitbit
##Also updates keys etc.	
def UpdateFitbitDataFunc(fitbiter):
	activity_data=GetFitbitData(fitbiter)
	
	distance_by_date=activity_data['activities-distance']
	for i in distance_by_date:
		fitdata=FitData(fitbiter=fitbiter,
				date=i['dateTime'],
				distance=i['value'],
				)
		fitdata.save()
	return

##Works only for 1 fitbiter at a time!
class FitDataDisplayView(TemplateView):
	template_name="fitdata/fitdata_display.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		##Retrieves what data needs to be displayed based on Form from FitDataIndex
		num_days=int(kwargs['num_days'])
		
		fitbiter_ids=kwargs['fitbiter_ids'] 
		fitbiter_ids=eval(fitbiter_ids)

		##for fitbiter_id in fitbiter_ids:
		fitbiters=Fitbiter.objects.filter(pk__in=fitbiter_ids)
			
		for fitbiter in fitbiters:
			UpdateFitbitDataFunc(fitbiter)
		
		today = datetime.date.today()
##If Fitbiter has less than num of days selected will cut of newest dates

		ago = today - datetime.timedelta(days=(num_days-1))
		
		fitdata=FitData.objects.filter(fitbiter__in=fitbiters, date__gte=ago).order_by('date')
		
		fitdata_list=[]
		first=True
		for fitbiter in fitbiters:
			if first:
				fitdata_list.append(fitdata.filter(fitbiter=fitbiter).values_list('date', flat=True))
				first=False
			fitdata_list.append(fitdata.filter(fitbiter=fitbiter).values_list('distance', flat=True))
		
		zipped_fitdata=list(zip(*fitdata_list))
		
		data_table=[list(x) for x in zipped_fitdata]

		context['today']=today
		context['ago']=ago
		context['fitbiters']=fitbiters
		context['data_table']=data_table
		return context