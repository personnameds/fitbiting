from django.urls import path
from rundata.views import RunDataIndexView, RunDataDisplayView

urlpatterns = [
	path('', RunDataIndexView.as_view(), name='rundata-index'),
	path('displaydata/<str:runner_ids>/<int:num_days>/', RunDataDisplayView.as_view(), name='rundata-display'),
]
