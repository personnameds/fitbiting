from django.urls import path
from runmap.views import RunMapIndex, DisplayRouteTemplateView, CreateRouteFormView
from runmap.views import FinishedRoute, DisplayFinishedRouteTemplateView

urlpatterns = [
	path('', RunMapIndex.as_view(), name='runmap-index'),
	path('createroute/', CreateRouteFormView.as_view(), name='createroute'),
	path('displaymap/<int:route>/', DisplayRouteTemplateView.as_view(), name='displayroute'),
	path('displayfinishedroute/<int:route>/', DisplayFinishedRouteTemplateView.as_view(), name='displayfinishedroute'),
	path('finishedroute/<int:route>/', FinishedRoute, name='finishedroute'),
]
