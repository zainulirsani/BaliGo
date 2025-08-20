from django import forms
from ..models import *

class MapsApiForm(forms.ModelForm):
	class Meta:
		model = MapsApi
		fields = ['api']

		widgets = {
			'api': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Daata API'}),
		}

		labels = {
			'Api': 'API Key',
		}