from django.urls import path
from django.views.generic import TemplateView
from oauth2.views import Oauth2View

urlpatterns = [
	path('', TemplateView.as_view(template_name="fitbiters/fitbiters_index.html"), name='fitbiters-index'),
	path('add_fitbiter/', Oauth2View, name='new_fitbiter'),
]
