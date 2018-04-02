from django.contrib import admin
from .models import FitData

class DistanceFilter(admin.SimpleListFilter):
	title='distance'
	parameter_name='distance'
	
	def lookups(self, request, model_admin):
		return (
			('<1','less than 1 km'),
			('<5','1 to 5 km'),
			('<10','5 to 10 km'),
			('<20','10 to 20 km'),
			('>20','20 km or more'),
			)
	def queryset(self, request, queryset):
		if self.value() == '<1':
			return queryset.filter(distance__lt=1)
		if self.value() == '<5':
			return queryset.filter(distance__gte=1, distance__lt=5)
		if self.value() == '<10':
			return queryset.filter(distance__gte=5, distance__lt=10)
		if self.value() == '<20':
			return queryset.filter(distance__gte=10, distance__lt=20)
		if self.value() == '>20':
			return queryset.filter(distance__gte=20)
		
class FitDataAdmin(admin.ModelAdmin):
	list_display=('fitbiter','date','distance')
	date_hierarchy='date'
	list_filter=('fitbiter','date',DistanceFilter)
	

admin.site.register(FitData,FitDataAdmin)
