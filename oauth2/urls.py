from django.urls import path
from oauth2.views import Oauth2View, Oauth2CallBackView

urlpatterns = [
    path('', Oauth2View, name='oauth2-view'),
    path('oauth2callback/', Oauth2CallBackView, name='oauth2callback-view'),
]
