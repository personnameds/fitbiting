from django import forms
from fitmap.models import FitRoute
from fitbiters.models import Fitbiter

class FitDataForm(forms.Form):
	fitbiters=forms.ModelChoiceField(queryset=Fitbiter.objects.all(),required=True, empty_label=None)
