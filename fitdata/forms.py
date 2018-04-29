from django import forms
from fitmap.models import FitRoute
from fitbiters.models import Fitbiter

class FitDataForm(forms.Form):
	routes=forms.ModelChoiceField(queryset=FitRoute.objects.all(),required=False)
	all_fitbiters=forms.BooleanField(label='Choose All People', required=False)
	fitbiters=forms.ModelMultipleChoiceField (queryset=Fitbiter.objects.all(), widget=forms.CheckboxSelectMultiple,required=False)
	
	def clean(self):
		cleaned_data=super().clean()
		routes=cleaned_data.get('routes')
		fitbiters=cleaned_data.get('fitbiters')
		all_fitbiters=cleaned_data.get('all_fitbiters')
		
		if routes and fitbiters and all_fitbiters:
			raise forms.ValidationError('Only need to choose ONE OF either route or people')
		elif not routes and not fitbiters and not all_fitbiters:
			raise forms.ValidationError('Need to choose either a route or people')
		elif all_fitbiters and fitbiters:
			raise forms.ValidationError('Do you want all people or just a few?')
	
	
	
