from django.urls import path
from oauth2.views import FitbitCallBackView, StravaCallBackView

urlpatterns = [
    path('fitbitcallback/', FitbitCallBackView),
    path('stravacallback/', StravaCallBackView),
]
