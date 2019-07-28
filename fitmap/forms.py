from django import forms
from fitmap.models import FitRoute
from fitbiters.models import Fitbiter

class FitMapForm(forms.Form):
	routes=forms.ModelChoiceField(queryset=FitRoute.objects.all(),required=False, empty_label=None)

class CreateRouteForm_MapDetails(forms.Form):
	title=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id':"title"}))
	start=forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id':"start"}))
	end=forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id':"end"}))
	
	