from django.shortcuts import render

from django.views.generic import TemplateView
from runmap.models import Route
from rundata.models import RunData
from django.db.models import Sum

from datetime import datetime, date, timedelta

class HomepageView(TemplateView):
	template_name="homepage/homepage.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['current_list'] = Route.objects.filter(finished=False)
		context['completed_list'] = Route.objects.filter(finished=True)
		
		distance_list=[]
		today = date.today()
		for i in range(0,7):
			d=today - timedelta(days=i)
			distance = RunData.objects.filter(date=d).aggregate(Sum('distance'))
			distance = distance['distance__sum'] or 0
			distance_list.append((d, distance))

		context['distance_list']=distance_list
		return context