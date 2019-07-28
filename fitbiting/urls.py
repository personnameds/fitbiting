from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('', include('homepage.urls')),
	path('fitdata/', include('fitdata.urls')),
	path('fitmap/', include('fitmap.urls')),
	path('fitbiters/', include('fitbiters.urls')),
	path('oauth2/', include('oauth2.urls')),
    path('admin/', admin.site.urls),
]
