from django.urls import path
from fitmap.views import FitMapIndex, DisplayRouteTemplateView
from fitmap.views import CreateRoute_SaveRoute, CreateRouteFormView, SaveMappedRoute

urlpatterns = [
	path('', FitMapIndex.as_view(), name='fitmap-index'),
	path('createroute/', CreateRouteFormView.as_view(), name='createroute'),
	path('createroute/saveroute', CreateRoute_SaveRoute, name='createroute_saveroute'),
	#Used for saving a route and displaying a route 
	path('savemappedroute', SaveMappedRoute, name='savemappedroute'),
	path('displaymap/<str:fitroute>/', DisplayRouteTemplateView.as_view(), name='displayroute'),
]
