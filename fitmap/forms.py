from django import forms
from fitmap.models import FitRoute
from fitbiters.models import Fitbiter

COLOUR_CHOICES=(
	(None,'---------'),
	('#e6194b','Red'),
	('#3cb44b','Green'),
	('#ffe119','Yellow'),
	('#0082c8','Blue'),
	('#f58231','Orange'),
	('#911eb4','Purple'),
	('#46f0f0','Cyan'),
	('#f032e6','Magenta'),
	('#e6beff','Lavender'),
	('#000080','Navy'),
	)

class FitMapForm(forms.Form):
	routes=forms.ModelChoiceField(queryset=FitRoute.objects.all(),required=False)


##Form for choosing fitbiters and their colour choice
##Will do this after creating the route


# class CreateRouteForm(forms.Form):
# 	fitbiter=forms.ModelChoiceField(queryset=Fitbiter.objects.all())
# 	colour=forms.ChoiceField(choices=COLOUR_CHOICES)
# 	
# 	def clean(self):
# 		cleaned_data=super().clean()
# 		colour=cleaned_data.get('colour')
# 		fitbiter=cleaned_data.get('fitbiter')
# 		
# 		if colour and not fitbiter:
# 			raise forms.ValidationError('Who does this colour represents?')
# 		elif not colour and fitbiter:
# 			raise forms.ValidationError('Need to choose a colour for this person.')

		
		