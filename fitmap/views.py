from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from django.views.generic import TemplateView
from .models import FitRoute, FitMappedRte, WayPoint
from fitdata.models import FitData
from fitdata.views import UpdateFitbitDataFunc
from fitbiters.models import Fitbiter
from datetime import datetime

def FitMapIndex(request):
	##I could use a view here to choose routes
	fitroute=FitRoute.objects.get(name="Sudeep to Neel")
	if FitMappedRte.objects.filter(fitroute=fitroute).exists():
		return redirect('display-fitmap-view')
	else:
		return redirect('startmap-view')

class DisplayFitMapView(TemplateView):
	template_name="fitmap/displayfitmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		##Update all fitbit data for all users
		#Later this should be only for user involved in this route
		UpdateFitbitDataFunc()		
		
		##TO DO Hard Coded for Now
		##Can come from index view
		fitroute=FitRoute.objects.get(name="Sudeep to Neel")
		

		##Get FitData from latest update but not including today
		##Does not include today, because it will update today's data
		##Gets from all users, later should be only for users involved in routes
		latest_update=FitMappedRte.objects.filter(fitroute=fitroute).latest('date').date
		fitdata=FitData.objects.filter(date__gte=latest_update, distance__gt=0)
		mappedrte_all=FitMappedRte.objects.filter(fitroute=fitroute).order_by('order')
		latest_order=FitMappedRte.objects.filter(fitroute=fitroute).latest('order').order
		
		context['order']=latest_order+1
		context['fitdata_all']=fitdata
		context['mappedrte_all'] = mappedrte_all
		context['fitroute']=fitroute
		context['waypoints']=fitroute.waypoints.all().order_by('order')[fitroute.num_complete_waypt:]
		return context

class StartMapView(TemplateView):
	template_name="fitmap/startmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		##Update all fitbit data for all users
		#Later this should be only for user involved in this route
		UpdateFitbitDataFunc()
		
		##TO DO Hard Coded for Now
		##Can come from index view
		fitroute=FitRoute.objects.get(name="Sudeep to Neel")
		
		
		##Will start with today's data only
		date=datetime.now() ##normal
		date=datetime.strptime("2018-04-03", "%Y-%m-%d").date() ##for testing purposes because my fitbit broke
		
		##Takes all data from today from all Fitbiters
		context['fitdata_all']=FitData.objects.filter(date=date, distance__gt=0)
		context['fitroute']=fitroute
		context['waypoints']=fitroute.waypoints.all().order_by('order')
		return context
 
def SaveFitMappedRte(request):
	encodedPath=request.GET.get('encodedPath')
	fitroute_name=request.GET.get('fitroute')
	fitbiter_id=request.GET.get('fitbiter')
	strokecolor=request.GET.get('strokecolor')
	order=request.GET.get('order')
	num_complete_waypt=int(request.GET.get('num_complete_waypt'))

	fitroute=FitRoute.objects.get(name=fitroute_name)
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


