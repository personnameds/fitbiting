from django.urls import path
from runmap.views import RunMapIndex, DisplayRouteTemplateView, CreateRouteFormView
from runmap.views import FinishedRoute, DisplayFinishedRouteTemplateView

urlpatterns = [
	path('', RunMapIndex.as_view(), name='runmap-index'),
	path('createroute/', CreateRouteFormView.as_view(), name='createroute'),
	path('displaymap/<str:route>/', DisplayRouteTemplateView.as_view(), name='displayroute'),
	path('displayfinishedmap/<str:route>/', DisplayFinishedRouteTemplateView.as_view(), name='displayfinishedroute'),
	path('finishedroute/<str:route>/<str:finished>/', FinishedRoute, name='finishedroute'),
]
