from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.http import JsonResponse
from datetime import date, timedelta, datetime

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .models import FitRoute, FitRunner
from fitdata.models import FitData

from .forms import FitMapForm, CreateRouteForm_MapDetails

from fitdata.views import UpdateFitbitDataFunc
from fitbiters.models import Fitbiter

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Sum

##Update a map or create a new map
class FitMapIndex(FormView):
	template_name='fitmap/fitmap_form.html'
	form_class=FitMapForm
	
	def form_valid(self, form):
		if 'create' in self.request.POST:
			return redirect('createroute')
		else:
			self.fitroute=form.cleaned_data['routes']
			if self.fitroute.finished==True:
				return redirect(reverse('displayfinishedroute', kwargs={'fitroute':self.fitroute.pk}))
			return HttpResponseRedirect(self.get_success_url())
		
	def get_success_url(self):
		return reverse('displayroute', kwargs={'fitroute':self.fitroute.pk})
			

class CreateRouteFormView(FormView):
	form_class=CreateRouteForm_MapDetails
	template_name='fitmap/createmap_form.html'
	
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
		
		fitbiters = form.cleaned_data['fitbiters']

		fitroute=FitRoute(title=title,
			start_lat=start_lat,
			start_long=start_long,
			end_lat=end_lat,
			end_long=end_long,
			start_date=date.today()
			)
		fitroute.save()
		
		i=0;
		for fitbiter in fitbiters:
			fitrunner=FitRunner(fitbiter=fitbiter, 
					   			colour=strokecolor[i],
					   			fitroute=fitroute,
					   			)
			fitrunner.save()
			i += 1
					
		self.fitroute=fitroute


		return super().form_valid(form)
	
	def get_success_url(self):
		return reverse('displayroute', kwargs={'fitroute':self.fitroute.pk})

class DisplayRouteTemplateView(TemplateView):
	template_name="fitmap/displayfitmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		fitroute=FitRoute.objects.get(pk=kwargs['fitroute'])
		start_date=fitroute.start_date
		
		fitrunners=FitRunner.objects.filter(fitroute=fitroute)

		fitbiters=Fitbiter.objects.filter(pk__in=fitrunners.values_list('fitbiter'))
		fitdata_all=FitData.objects.filter(fitbiter__in=fitbiters, date__gte=start_date).order_by('-date')

		##Data for map
		#Data from FitDate after or same date as last update
		fitdata_list=[]
		for fitrunner in fitrunners:
			#Get and update each fitbiter involved in the route
			fitbiter=Fitbiter.objects.get(fitbit_id=fitrunner.fitbiter)
			UpdateFitbitDataFunc(fitbiter, start_date)
			
			fitdata=fitdata_all.filter(fitbiter=fitbiter, date__gte=start_date).order_by('-date')
			for f in fitdata:
				fitdata_list.append((f.date, fitrunner, f)) 


		#Orders the list by fitrunner by date
		fitdata_list.sort(key=lambda x:x[0])

		##Data for Charts
		week_ago=date.today()-timedelta(days=7)
		#Data for Stacked Bar Chart
		dates=fitdata_all.filter(date__gte=week_ago).values_list('date', flat=True).order_by('-date').distinct() ##Need to include order_by for database????

		data_table=[]
		for d in dates:
			dt=[d]
			dt.extend(fitdata_all.filter(date=d).values_list('distance', flat=True).order_by('fitbiter'))
			data_table.append(dt)
		
		pie_data_table=[]
		for fitrunner in fitrunners:
			dist=fitdata_all.filter(fitbiter=fitrunner.fitbiter).aggregate(Sum('distance'))
			dist=dist['distance__sum']
			pie_data_table.append([fitrunner.fitbiter,dist])
		
		context['today']=date.today()
		context['fitrunners']=list(fitrunners)
		context['data_table']=data_table
		context['pie_data_table']=pie_data_table
		context['fitdata_list']=fitdata_list
		context['fitroute']=fitroute
		context['API_KEY']=settings.API_KEY
		return context


##THIS DOESN'T WORK ANYMORE
class DisplayFinishedRouteTemplateView(TemplateView):
	template_name="fitmap/finishedfitmap.html"
	
#Used for creating a route and displaying a route
def FinishedRoute(request, finished, fitroute):
	pass

##ABOVE DOESN'T WORK ANYMORE