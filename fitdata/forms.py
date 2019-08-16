from django import forms
from fitmap.models import FitRoute
from fitbiters.models import Fitbiter

class FitDataForm(forms.Form):
	fitbiters=forms.ModelMultipleChoiceField(queryset=Fitbiter.objects.all(),
											 widget=forms.CheckboxSelectMultiple,
											 required=True,
											 error_messages={'required': 'Please choose at least one person'},
											 )
	num_days=forms.IntegerField(min_value=1, 
								max_value=10,
								initial=5, 
								widget=forms.NumberInput,
								label='How many days of data to graph? (1-10 days)',
								)
