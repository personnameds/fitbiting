from django import forms
from runmap.models import Route
from runners.models import Runner
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Button

class RunMapForm(forms.Form):
	routes=forms.ModelChoiceField(queryset=Route.objects.order_by('start_date').order_by('finished'),required=False, empty_label=None)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('display', 'Display Selected Route'))
		self.helper.add_input(Submit('create', 'Create New Route'))

class CreateRouteForm_MapDetails(forms.Form):
	title=forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id':"title",'size':'30%'}))
	start=forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id':"start",'size':'30%'}))
	end=forms.CharField(max_length=250, widget=forms.TextInput(attrs={'id':"end",'size':'30%'}))
	runners=forms.ModelMultipleChoiceField(queryset=Runner.objects.all(), 
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
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Button('check', 'Check Route', css_id='check', css_class='btn-info'))
		self.helper.add_input(Submit('save', 'Save Route'))		
		self.fields['runners'].label_from_instance = self.label_from_instance
	
	def label_from_instance(self, obj):
		return obj.user.username