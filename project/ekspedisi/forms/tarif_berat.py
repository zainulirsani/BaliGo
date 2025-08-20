from django import forms
from ..models import *


class TarifBeratForm(forms.ModelForm):
	class Meta:
		model = TarifBerat
		fields = ['id_tarif_berat', 'berat', 'tarif', ]

		widgets = {
			'berat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan berat (Kilogram)', 'id': 'inputBerat', 'required': True}),
			'tarif': forms.TextInput(attrs={'class': 'form-control tarif', 'placeholder': 'Masukan Tarif (Rp.)', 'id': 'inputTarif', 'required': True})
		}

		labels = {
			'berat': 'Berat',
			'tarif': 'Tarif'
		}