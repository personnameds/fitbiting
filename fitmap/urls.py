from django.urls import path
from fitmap.views import FitMapIndex, DisplayFitMapView
from fitmap.views import CreateRoute_SaveRoute, CreateRouteFormView, CreateRoute_SaveMappedRoute

urlpatterns = [
	path('', FitMapIndex.as_view(), name='fitmap-index'),
	path('createroute/', CreateRouteFormView.as_view(), name='createroute'),
	path('createroute/saveroute', CreateRoute_SaveRoute, name='createroute_saveroute'),
	#Used for saving a route and displaying a route 
	path('createroute/mappedroute', CreateRoute_SaveMappedRoute, name='createroute_savemappedroute'),
	path('displaymap/<str:fitroute>/', DisplayFitMapView.as_view(), name='display-fitmap-view'),
]
