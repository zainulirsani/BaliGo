from django import forms
from ..models import *


class TarifKilometerForm(forms.ModelForm):
	class Meta:
		model = TarifKilometer
		fields = ['id_tarif_kilometer', 'jarak', 'tarif', ]

		widgets = {
			'jarak': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Jarak (Kilometer)', 'id': 'inputJarak', 'required': True}),
			'tarif': forms.TextInput(attrs={'class': 'form-control tarif', 'placeholder': 'Masukan Tarif (Rp.)', 'id': 'inputTarif', 'required': True})
		}

		labels = {
			'jarak': 'Jarak',
			'tarif': 'Tarif'
		}