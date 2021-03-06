from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class NewRunnerForm(forms.Form):
	first_name=forms.CharField(max_length=50, label='First Name')
	username=forms.CharField(max_length=50, label='Username', help_text='The name people will see.')
	goal=forms.DecimalField(max_digits=6, decimal_places=2, label='Daily Goal in KM', help_text="How may KM would you like to walk/run in a day?")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Join'))
