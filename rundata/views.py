from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from oauth2.views import UpdateRunData
from runners.models import Runner
from rundata.models import RunData
from rundata.forms import RunDataForm

import datetime


##Form that asks what data should be displayed
class RunDataIndexView(FormView):
	template_name='rundata/rundata_form.html'
	form_class=RunDataForm

	def form_valid(self, form):
		runners = form.cleaned_data['runners']
		runner_ids=[]
		for runner in runners:
			runner_ids.append(runner.pk)
		self.runner_ids=runner_ids
		self.num_days=form.cleaned_data['num_days']
		return super().form_valid(form)
		
	def get_success_url(self):
		return reverse('rundata-display', kwargs={'runner_ids':self.runner_ids,'num_days':self.num_days})

##Works only for 1 fitbiter at a time!
class RunDataDisplayView(TemplateView):
	template_name="rundata/rundata_display.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		##Retrieves what data needs to be displayed based on Form from FitDataIndex
		num_days=int(kwargs['num_days'])
		
		runner_ids=kwargs['runner_ids'] 
		runner_ids=eval(runner_ids)

		##for fitbiter_id in fitbiter_ids:
		runners=Runner.objects.filter(pk__in=runner_ids)

		today = datetime.date.today()
##If Fitbiter has less than num of days selected will cut of newest dates
##This date thing doesn't work when Strava and Fitbit mixed, it cuts off dates??
		ago = today - datetime.timedelta(days=(num_days-1))
			
		for runner in runners:
			UpdateRunData(runner, ago)
		
		rundata=RunData.objects.filter(runner__in=runners, date__gte=ago).order_by('date')
		
		rundata_list=[]
		first=True
		for runner in runners:
			if first:
				rundata_list.append(rundata.filter(runner=runner).values_list('date', flat=True))
				first=False
			rundata_list.append(rundata.filter(runner=runner).values_list('distance', flat=True))
		
		zipped_rundata=list(zip(*rundata_list))
		
		data_table=[list(x) for x in zipped_rundata]

		context['today']=today
		context['ago']=ago
		context['runners']=runners
		context['data_table']=data_table
		return context