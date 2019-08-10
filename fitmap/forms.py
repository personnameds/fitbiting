from django import forms
from fitmap.models import FitRoute
from fitbiters.models import Fitbiter

class FitMapForm(forms.Form):
	routes=forms.ModelChoiceField(queryset=FitRoute.objects.all(),required=False, empty_label=None)

class CreateRouteForm_MapDetails(forms.Form):
	title=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id':"title",'size':'30%'}))
	start=forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id':"start",'size':'30%'}))
	end=forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id':"end",'size':'30%'}))
	fitbiters=forms.ModelMultipleChoiceField(queryset=Fitbiter.objects.all(), 
											 widget=forms.CheckboxSelectMultiple,
											 error_messages={'required': 'Please choose at least one person'},
											 )
	status=forms.CharField(max_length=5, initial=False, widget=forms.HiddenInput(attrs={'id':"status"}))
	start_lat=forms.DecimalField(max_digits=10, decimal_places=6, required=False, widget=forms.HiddenInput(attrs={'id':"start_lat"}))
	start_long=forms.DecimalField(max_digits=10, decimal_places=6, required=False, widget=forms.HiddenInput(attrs={'id':"start_long"}))
	end_lat=forms.DecimalField(max_digits=10, decimal_places=6, required=False, widget=forms.HiddenInput(attrs={'id':"end_lat"}))
	end_long=forms.DecimalField(max_digits=10, decimal_places=6, required=False, widget=forms.HiddenInput(attrs={'id':"end_long"}))

	def clean_status(self):
			status = self.cleaned_data['status']
			if status == 'False':
				raise forms.ValidationError("Check if your route is valid")
			return status