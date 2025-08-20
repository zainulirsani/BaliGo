from django import forms
from ..models import *


class JenisKirimanForm(forms.ModelForm):

	class Meta:
		model = JenisKiriman
		fields = ['nama']

		widgets = {
			'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'JenisKiriman', 'required': True})
		}

		labels = {
			'nama': 'Jenis Kiriman',
		}