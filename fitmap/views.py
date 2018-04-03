from django.shortcuts import render, redirect
from datetime import datetime
from django.views.generic import TemplateView
from .models import FitRoute, FitMappedRte

class FitMapView(TemplateView):
	template_name="fitmap/fitmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		##Hard Coded for Now
		fitroute=FitRoute.objects.get(name="Sudeep to Neel")		
		
		if FitMappedRte.objects.filter(fitroute=fitroute).exists():
			context['fitmappedrte']=FitMappedRte.objects.get(fitroute=fitroute)
		else:	
			a=DoSomethingElse
			context['fitroute'] = FitRoute.objects.get(name="Sudeep to Neel")
		
		##Get rid of later
		context['fitroute'] = FitRoute.objects.get(name="Sudeep to Neel")
		return context

def GetFitMappedRteView(request):
	encodedPath=request.GET.get('encodedPath')
	
	##Hard Coded for Now
	fitroute=FitRoute.objects.get(name="Sudeep to Neel")

	if FitMappedRte.objects.filter(fitroute=fitroute, date=datetime.today().date()).exists():
		fitmappedrte=FitMappedRte.objects.get(fitroute=fitroute, date=datetime.today().date())
		fitmappedrte.maprtedata=encodedPath
	else:
		fitmappedrte=FitMappedRte(fitroute=fitroute,
						date=datetime.today().date(),
						maprtedata=encodedPath,
						)
	fitmappedrte.save()
	return redirect('homepage-index')

class DisplayFitMappedRteView(TemplateView):
	template_name="fitmap/displayfitmap.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['fitmappedrte'] = FitMappedRte.objects.get(fitroute__name="Sudeep to Neel")
		return context