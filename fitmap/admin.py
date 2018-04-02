
from django.contrib import admin
from .models import StartPoint, EndPoint, WayPoint, FitRoute, FitMappedRte

admin.site.register(StartPoint)
admin.site.register(EndPoint)
admin.site.register(WayPoint)
admin.site.register(FitRoute)
admin.site.register(FitMappedRte)
