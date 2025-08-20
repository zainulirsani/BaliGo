from django import forms
from ..models import *


class TarifGudangForm(forms.ModelForm):

	def __init__(self, *args, **kwargs) :
		super(TarifGudangForm, self).__init__(*args, **kwargs)		
		# Berfungsi agar tidak meload data atau record dari model yg terforeign key (agar tidak berat saat meload template dengan form ini)
		self.fields['from_gudang'].choices = [('', "Ketik Nama Gudang/Alamat Gudang")]
		self.fields['to_gudang'].choices = [('', "Ketik Nama Gudang/Alamat Gudang")]


	class Meta:
		model = TarifGudang
		fields = ['id_tarif_gudang', 'from_gudang', 'to_gudang', 'tarif', ]

		widgets = {
			'from_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Dari Gudang Mana?', 'id': 'inputFromGudang', 'required': True}),
			'to_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Ke Gudang Mana?', 'id': 'inputToGudang', 'required': True}),
			'tarif': forms.TextInput(attrs={'class': 'form-control tarif', 'placeholder': 'Masukan Tarif (Rp.)', 'id': 'inputTarif', 'required': True})
		}

		labels = {
			'from_gudang': 'Dari Gudang',
			'to_gudang': 'Ke Gudang',
			'tarif': 'Tarif'
		}