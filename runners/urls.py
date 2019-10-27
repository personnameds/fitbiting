from django.urls import path
from .views import PlatformListView, NewRunnerFormView
from oauth2.views import NewRunnerView

urlpatterns = [
	path('', PlatformListView.as_view(), name='platform-index'),
	path('add_runner_form/<int:platform_id>', NewRunnerFormView.as_view(), name='new_runner_form'),
	path('add_runner_oauth2/<int:platform_id>', NewRunnerView, name='new_runner_oauth2'),
]
