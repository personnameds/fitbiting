"""fitbiting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from fitmap.views import FitMapIndex, StartMapView, SaveFitMappedRte, DisplayFitMapView, CreateRouteView

urlpatterns = [
	path('', FitMapIndex.as_view(), name='fitmap-index'),
	path('createroute', CreateRouteView.as_view(), name='createroute-view'),
	
	path('displaymap/', DisplayFitMapView.as_view(), name='display-fitmap-view'),
	path('startmap/', StartMapView.as_view(), name='startmap-view'),
    path('savemap/', SaveFitMappedRte, name='savefitmappedrte-view'),
]
