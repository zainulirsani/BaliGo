from django import forms
from ..models import *


class ExtraCashForm(forms.ModelForm):
	class Meta:
		model = ExtraCash
		fields = ['wilayah', 'tarif']

		widgets = {
			'wilayah': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Input Wilayah', 'id': 'inputWilayah', 'required': True}),
			'tarif': forms.TextInput(attrs={'class': 'form-control tarif', 'placeholder': 'Masukan Tarif (Rp.)', 'id': 'inputTarif', 'required': True})
		}

		labels = {
			'wilayah': 'Wilayah',
			'tarif': 'Tarif'
		}