from django.urls import reverse
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from oauth2.views import GetDataUsingAccessToken
from runners.models import Runner
from rundata.models import RunData
from rundata.forms import RunDataForm

from decimal import Decimal

from datetime import datetime, date, timedelta

def UpdateRunData(runner, update_date):
	activity_data = GetDataUsingAccessToken(runner, update_date) 
	
	##Fitbit
	if runner.platform.name == 'Fitbit':
		distance_by_date=activity_data['activities-distance']
		for i in distance_by_date:
			rundata, created=RunData.objects.get_or_create(runner=runner,
										  date=i['dateTime'],
										  )
			rundata.distance=Decimal(i['value'])
			#Do not want to overwrite goal that was created at that time
			#If created then add goal, otherwise keep the goal as is
			if created:
				rundata.goal=runner.goal
			rundata.goal_percent=rundata.distance/rundata.goal
			rundata.save()	
		return

	##Strava
	elif runner.platform.name == 'Strava':
		##Not tested
		for activity in activity_data:
			distance=Decimal(activity['distance']/1000)
			activity_date=datetime.strptime(activity['start_date_local'],"%Y-%m-%dT%H:%M:%SZ")
			if activity_date.date() >= update_date:
				rundata, created = RunData.objects.get_or_create(runner=runner,
															  date=activity_date.date(),
															  )
				rundata.distance=distance
				if created:
					rundata.goal=runner.goal
				a=rundata.goal
				rundata.goal_percent=rundata.distance/rundata.goal
				rundata.save()
		return

def UpdateGoal(runner):
	if date.today() - timedelta(days=14) >= runner.goal_set_date:		
		reached_goal=RunData.objects.filter(
					runner=runner, 
					date__gte=runner.goal_set_date,
					goal_percent__gte=1, 
					).count()
		if reached_goal >= 10:
			runner.goal = runner.goal*Decimal(1.1)
			runner.save()
		elif reached_goal <=4:
			runner.goal = runner.goal * Decimal(0.9)
			runner.save()
	return
	
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

		today = date.today()
##If Fitbiter has less than num of days selected will cut of newest dates
##This date thing doesn't work when Strava and Fitbit mixed, it cuts off dates??
		update_date = today - timedelta(days=(num_days))
			
		for runner in runners:
			UpdateRunData(runner, update_date)
			UpdateGoal(runner)
		
		rundata=RunData.objects.filter(runner__in=runners, date__gte=update_date).order_by('date')
		
		rundata_list=[]
		dates_list= [today - timedelta(days=x) for x in range(num_days,0,-1)]
		rundata_list.append(dates_list)
		for runner in runners:
			rundata_list.append(rundata.filter(runner=runner).values_list('distance', flat=True))
		zipped_rundata=list(zip(*rundata_list))
		
		data_table=[list(x) for x in zipped_rundata]

		context['today']=today
		context['update_date']=update_date
		context['runners']=runners
		context['data_table']=data_table
		return context