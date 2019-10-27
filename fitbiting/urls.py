from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	path('', include('homepage.urls')),
	path('rundata/', include('rundata.urls')),
	path('runmap/', include('runmap.urls')),
	path('runners/', include('runners.urls')),
	path('oauth2/', include('oauth2.urls')),
    path('admin/', admin.site.urls),
]
