from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.http import JsonResponse
from datetime import datetime

from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .models import FitRoute, FitMappedRte
from fitdata.models import FitData

from .forms import FitMapForm, CreateRouteForm_MapDetails

from fitdata.views import UpdateFitbitDataFunc
from fitbiters.models import Fitbiter


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
		return reverse('display-fitmap-view', kwargs={'fitroute':self.fitroute})
			

class CreateRouteFormView(FormView):
	form_class=CreateRouteForm_MapDetails
	template_name='fitmap/createmap_form.html'
	success_url='/'
	
	def get_initial(self):
		initial=super().get_initial()
		initial['title']='Sudeep to Neel'
		initial['start']='30 Elsie Lane'
		initial['end']='2182 Meadowglen Drive'
		return initial

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		#Update all fitbit data for all users
		#Later this should be only for user involved in this route
		fitbiters=Fitbiter.objects.all()
		UpdateFitbitDataFunc(fitbiters)
		
		#Starting data will be from today 
		date=datetime.now()
		
		context['fitdata_all']=FitData.objects.filter(date=date, distance__gt=0)
		return context
		
	
def CreateRoute_SaveRoute(request):
	title=request.GET.get('title')
	start_lat=request.GET.get('start_lat')
	start_long=request.GET.get('start_long')
	end_lat=request.GET.get('end_lat')
	end_long=request.GET.get('start_long')	
	
	fitroute=FitRoute(title=title,
		start_lat=start_lat,
		start_long=start_long,
		end_lat=end_lat,
		end_long=end_long,
		)
	fitroute.save()
	
	## I don't actually do anything with this success
	return JsonResponse({'response':'success'})	


#Used for creating a route and displaying a route
def CreateRoute_SaveMappedRoute(request):
	encodedPath=request.GET.get('encodedPath')
	fitroute_title=request.GET.get('fitroute')
	fitbiter_id=request.GET.get('fitbiter')
	strokecolor=request.GET.get('strokecolor')
	order=request.GET.get('order')
	num_complete_waypt=int(request.GET.get('num_complete_waypt'))

	fitroute=FitRoute.objects.get(title=fitroute_title)
	fitbiter=Fitbiter.objects.get(fitbit_id=fitbiter_id)
	date_today=datetime.today().date()

	fitroute.num_complete_waypt=num_complete_waypt
	fitroute.save()

	if FitMappedRte.objects.filter(fitroute=fitroute,fitbiter=fitbiter,date=date_today).exists():
		fitmappedrte=FitMappedRte.objects.get(fitroute=fitroute, fitbiter=fitbiter, date=date_today)
		fitmappedrte.maprtedata=encodedPath
		fitmappedrte.colour=strokecolor
		fitmappedrte.order=order
	else:
		##Save the Mapped Route for that fitbiter and fitroute
		fitmappedrte=FitMappedRte(fitroute=fitroute,
							fitbiter=fitbiter,
							date=date_today,
							maprtedata=encodedPath,
							colour=strokecolor,
							order=order,
						)
		fitmappedrte.save()
	
	return JsonResponse({'response':'success'}) ##returned by not captured, not sure what happens with it?

class DisplayFitMapView(TemplateView):
	template_name="fitmap/displayfitmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		fitroute=FitRoute.objects.get(title=kwargs['fitroute'])

		#Update all fitbit data for all users
		#Later this should be only for user involved in this route
		fitbiters=Fitbiter.objects.all()
		UpdateFitbitDataFunc(fitbiters)	
		
		##Get FitData from last update but not including today
		##Does not include today, because it will update today's data
		##Gets from all users, later should be only for users involved in routes
		last_update=FitMappedRte.objects.filter(fitroute=fitroute).latest('date').date
		fitdata=FitData.objects.filter(date__gte=last_update, distance__gt=0)
		mappedrte_all=FitMappedRte.objects.filter(fitroute=fitroute).order_by('order')
		last_order_num=FitMappedRte.objects.filter(fitroute=fitroute).latest('order').order
		
		context['order']=last_order_num+1
		context['fitdata_all']=fitdata
		context['mappedrte_all'] = mappedrte_all
		context['fitroute']=fitroute
		#context['waypoints']=fitroute.waypoints.all().order_by('order')[fitroute.num_complete_waypt:]
		return context


