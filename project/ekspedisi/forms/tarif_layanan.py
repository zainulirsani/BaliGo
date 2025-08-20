from django import forms
from ..models import *


class TarifLayananForm(forms.ModelForm):
	def __init__(self, *args, **kwargs) :
		super(TarifLayananForm, self).__init__(*args, **kwargs)
		self.fields['layanan'].choices = [('', "Pilih Layanan")]

	class Meta:
		model = TarifLayanan
		fields = ['id_tarif_layanan', 'layanan', 'tarif', ]

		widgets = {
			'layanan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Layanan', 'id': 'inputLayanan', 'required': True}),
			'tarif': forms.TextInput(attrs={'class': 'form-control tarif', 'placeholder': 'Masukan Tarif (Rp.)', 'id': 'inputTarif', 'required': True})
		}

		labels = {
			'layanan': 'Nama Layanan',
			'tarif': 'Tarif'
		}