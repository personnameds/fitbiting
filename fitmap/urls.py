from django.urls import path
from fitmap.views import FitMapIndex, DisplayRouteTemplateView, CreateRouteFormView, SaveMappedRoute
from fitmap.views import FinishedRoute, DisplayFinishedRouteTemplateView

urlpatterns = [
	path('', FitMapIndex.as_view(), name='fitmap-index'),
	path('createroute/', CreateRouteFormView.as_view(), name='createroute'),
	#Used for saving a route and displaying a route 
	path('savemappedroute', SaveMappedRoute, name='savemappedroute'),
	path('displaymap/<str:fitroute>/', DisplayRouteTemplateView.as_view(), name='displayroute'),
	path('displayfinishedmap/<str:fitroute>/', DisplayFinishedRouteTemplateView.as_view(), name='displayfinishedroute'),
	path('finishedroute/<str:fitroute>/<str:finished>/', FinishedRoute, name='finishedroute'),
]
