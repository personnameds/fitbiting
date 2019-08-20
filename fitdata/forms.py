from django import forms
from fitmap.models import FitRoute
from fitbiters.models import Fitbiter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FitDataForm(forms.Form):
	fitbiters=forms.ModelMultipleChoiceField(queryset=Fitbiter.objects.all(),
											 widget=forms.CheckboxSelectMultiple,
											 required=True,
											 error_messages={'required': 'Please choose at least one person'},
											 )
	num_days=forms.IntegerField(min_value=1, 
								max_value=10,
								initial=5, 
								widget=forms.NumberInput(attrs={'style':'max-width: 21em'}),
								label='How many days of data to graph? (1-10 days)',
								)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Show Distance Data'))
