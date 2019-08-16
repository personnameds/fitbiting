from django.urls import path
from fitdata.views import FitDataIndexView, FitDataDisplayView

urlpatterns = [
	path('', FitDataIndexView.as_view(), name='fitdata-index'),
	path('displaydata/<str:fitbiter_ids>/<int:num_days>/', FitDataDisplayView.as_view(), name='fitdata-display'),
]
