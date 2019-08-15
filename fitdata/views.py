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
		self.fitbiter = form.cleaned_data['fitbiters']
		return HttpResponseRedirect(self.get_success_url())
		
	def get_success_url(self):
		return reverse('fitdata-display', kwargs={'fitbiter_id':self.fitbiter})
		
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
		fitbiter_id=kwargs['fitbiter_id']
		
		#Only sending single fitbiter
		fitbiter=Fitbiter.objects.get(fitbit_id=fitbiter_id)

		##Based on data displays calls the UpdateFitbitData Function
		UpdateFitbitDataFunc(fitbiter)
		
		##Works only for 1 fitbiter at a time!
		data_table=FitData.objects.filter(fitbiter=fitbiter).order_by('-date')[:5]


		context['fitbiter']=fitbiter
		context['data_table']=data_table
		return context