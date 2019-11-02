from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.http import JsonResponse
from datetime import date, timedelta, datetime

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .models import Route, RteRunner
from rundata.models import RunData

from .forms import RunMapForm, CreateRouteForm_MapDetails

from rundata.views import UpdateRunData, UpdateGoal
from runners.models import Runner

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Sum

##Update a map or create a new map
class RunMapIndex(FormView):
	template_name='runmap/runmap_form.html'
	form_class=RunMapForm
	
	def form_valid(self, form):
		if 'create' in self.request.POST:
			return redirect('createroute')
		else:
			self.route=form.cleaned_data['routes']
			if self.route.finished==True:
				return redirect(reverse('displayfinishedroute', kwargs={'route':self.route.pk}))
			return HttpResponseRedirect(self.get_success_url())
		
	def get_success_url(self):
		return reverse('displayroute', kwargs={'route':self.route.pk})
			

class CreateRouteFormView(FormView):
	form_class=CreateRouteForm_MapDetails
	template_name='runmap/createmap_form.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['API_KEY']=settings.API_KEY
		return context
	
	def form_valid(self, form):
		strokecolor=["#0082c8","#3cb44b","#911eb4","#000080","#46f0f0#","#f58231","#f032e6","#e6beff"]
		
		title=form.cleaned_data['title']

		start_lat=form.cleaned_data['start_lat']
		start_long=form.cleaned_data['start_long']
		end_lat=form.cleaned_data['end_lat']
		end_long=form.cleaned_data['end_long']
		
		runners = form.cleaned_data['runners']

		route=Route(title=title,
			start_lat=start_lat,
			start_long=start_long,
			end_lat=end_lat,
			end_long=end_long,
			start_date=date.today()
			)
		route.save()
		
		i=0;
		for runner in runners:
			rterunner=RteRunner(runner=runner, 
					   			colour=strokecolor[i],
					   			route=route,
					   			)
			rterunner.save()
			i += 1
					
		self.route=route


		return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('displayroute', kwargs={'route':self.route.pk})

class DisplayRouteTemplateView(TemplateView):
	template_name="runmap/displayrunmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		route=Route.objects.get(pk=kwargs['route'])
		start_date=route.start_date
		
		rterunners=RteRunner.objects.filter(route=route)

		runners=Runner.objects.filter(pk__in=rterunners.values_list('runner'))
		rundata_all=RunData.objects.filter(runner__in=runners, date__gte=start_date).order_by('-date')

		##Data for map
		#Data from FitDate after or same date as last update
		rundata_list=[]
		for rterunner in rterunners:
			#Get and update each fitbiter involved in the route
			runner=Runner.objects.get(rterunner=rterunner)
			UpdateRunData(runner, start_date)
			UpdateGoal(runner)
			
			rundata=rundata_all.filter(runner=runner, date__gte=start_date).order_by('-date')
			for rd in rundata:
				rundata_list.append((rd.date, rterunner, rd)) 

		#Orders the list by fitrunner by date
		rundata_list.sort(key=lambda x:x[0])

		##Data for Charts
		week_ago=date.today()-timedelta(days=7)
		#Data for Stacked Bar Chart
		dates=rundata_all.filter(date__gte=week_ago).values_list('date', flat=True).order_by('-date').distinct() ##Need to include order_by for database????

		data_table=[]
		for d in dates:
			dt=[d]
			dt.extend(rundata_all.filter(date=d).values_list('distance', flat=True).order_by('runner'))
			data_table.append(dt)
		
		pie_data_table=[]
		for rterunner in rterunners:
			dist=rundata_all.filter(runner=rterunner.runner).aggregate(Sum('distance'))
			dist=dist['distance__sum']
			pie_data_table.append([rterunner.runner.user.username,dist])
		
		context['today']=date.today()
		context['rterunners']=list(rterunners)
		context['data_table']=data_table
		context['pie_data_table']=pie_data_table
		context['rundata_list']=rundata_list
		context['route']=route
		context['API_KEY']=settings.API_KEY
		return context


##THIS DOESN'T WORK ANYMORE
class DisplayFinishedRouteTemplateView(TemplateView):
	template_name="runmap/finishedrunmap.html"
	
#Used for creating a route and displaying a route
def FinishedRoute(request, finished, route):
	pass

##ABOVE DOESN'T WORK ANYMORE