from django import forms
from runners.models import Runner
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class RunDataForm(forms.Form):
	runners=forms.ModelMultipleChoiceField(queryset=Runner.objects.all(),
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
		self.fields['runners'].label_from_instance = self.label_from_instance
	
	def label_from_instance(self, obj):
		return obj.user.username