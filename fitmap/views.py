from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.http import JsonResponse
from datetime import date, datetime

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .models import FitRoute, FitMappedRte, FitRunner
from fitdata.models import FitData

from .forms import FitMapForm, CreateRouteForm_MapDetails

from fitdata.views import UpdateFitbitDataFunc
from fitbiters.models import Fitbiter

from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

##Update a map or create a new map
class FitMapIndex(FormView):
	template_name='fitmap/fitmap_form.html'
	form_class=FitMapForm
	
	def form_valid(self, form):
		if 'create' in self.request.POST:
			return redirect('createroute')
		else:
			self.fitroute=form.cleaned_data['routes']
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
			last_update=date.today(),
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

def takeThird(elem):
	return elem[2]		

class DisplayRouteTemplateView(TemplateView):
	template_name="fitmap/displayfitmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		fitroute=FitRoute.objects.get(pk=kwargs['fitroute'])
		fitrunners=FitRunner.objects.filter(fitroute=fitroute)

##Only used for fitdata_all
		fitbiters=Fitbiter.objects.filter(pk__in=fitrunners.values_list('fitbiter'))
		
		last_update=fitroute.last_update
		fitroute.last_update=date.today()
		fitroute.save()

##Now used by both
		fitdata_all=FitData.objects.filter(fitbiter__in=fitbiters, date__gte=last_update).order_by('-date')

##This is for map
		fitdata_list=[]
		for fitrunner in fitrunners:
			UpdateFitbitDataFunc(fitrunner.fitbiter)
			##Get FitData from last update
			##Includes last_update, because needs to redo that in case more distance was added later that day
			##If last_update is today, will overwrite and update distance data as it changes
			##If route created today will also catch and begin to save distance data
			fitdata=fitdata_all.filter(fitbiter=fitrunner.fitbiter)
##			fitdata=FitData.objects.filter(fitbiter=fitrunner.fitbiter, date__gte=last_update).order_by('-date')
			for f in fitdata:
				fitdata_list.append((f.date, fitrunner, f)) 

		##Do I need this sort or can I just add order_by as above
		fitdata_list.sort(key=lambda x:x[0])
		

		##Need to check this and rewrite!
		##Gets all mapped rtes, except the initial
		mappedrte_all=FitMappedRte.objects.filter(fitroute=fitroute,date__lt=last_update).order_by('order')
		if mappedrte_all:
			last_order_num=mappedrte_all.reverse()[0].order
		else:
			last_order_num=0
		
		##Data for Stacked Bar Chart
		dates=fitdata.values_list('date', flat=True).distinct()
		data_table=[]
		for d in dates:
			data_table.append(d)
			data_table.extend(fitdata_all.filter(date=d).values_list('distance', flat=True).order_by('date','fitbiter'))

		context['fitrunners']=list(fitrunners)
		context['data_table']=data_table

		context['order']=last_order_num
		context['fitdata_list']=fitdata_list
		context['mappedrte_all'] = mappedrte_all
		context['fitroute']=fitroute
		#context['waypoints']=fitroute.waypoints.all().order_by('order')[fitroute.num_complete_waypt:]
		context['API_KEY']=settings.API_KEY
		return context

#Used for creating a route and displaying a route
def SaveMappedRoute(request):
	encodedPath=request.GET.get('encodedPath')
	fitroute_pk=request.GET.get('fitroute')
	fitrunner_pk=request.GET.get('fitrunner')
	strokecolor=request.GET.get('strokecolor')
	data_date=request.GET.get('date')
	order=int(request.GET.get('order'))
	order=order+1 ##increment order number before saving
	#num_complete_waypt=int(request.GET.get('num_complete_waypt'))
	

	fitroute=FitRoute.objects.get(pk=fitroute_pk)	
	fitrunner=FitRunner.objects.get(pk=fitrunner_pk)
	
	##Data date is the date this fitbit data is from, may be different then actual date
	data_date=datetime.strptime(data_date, '%b. %d, %Y')

	if FitMappedRte.objects.filter(fitroute=fitroute,fitrunner=fitrunner,date=data_date).exists(): ##If exists then need to update distance
		fitmappedrte=FitMappedRte.objects.get(fitroute=fitroute, fitrunner=fitrunner, date=data_date)
		fitmappedrte.maprtedata=encodedPath
		## Order number should not change
		##fitmappedrte.order=order				
	else:
		##Save the Mapped Route for that fitbiter and fitroute
		fitmappedrte=FitMappedRte(fitroute=fitroute,
							fitrunner=fitrunner,
							date=data_date,
							maprtedata=encodedPath,
							order=order,
						)
	fitmappedrte.save()
	
	return JsonResponse({'response':'success'}) ##returned by not captured, not sure what happens with it?


