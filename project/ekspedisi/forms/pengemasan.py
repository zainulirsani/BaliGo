from django import forms
from ..models import *


class PengemasanForm(forms.ModelForm):
	class Meta:
		model = Pengemasan
		fields = ['id_pengemasan', 'nama_pengemasan', 'bahan_pengemasan', 'tarif']

		widgets = {
			'nama_pengemasan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Nama Pengemasan', 'id': 'inputNama'}),
			'bahan_pengemasan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Bahan Pengemasan', 'id': 'inputBahanPengemasan'}),
			'tarif': forms.TextInput(attrs={'class': 'form-control tarif', 'placeholder': 'Masukan Tarif Pengemasan', 'id': 'inputTarifPengemasan'})
		}

		labels = {
			'nama_pengemasan': 'Nama Pengemasan',
			'bahan_pengemasan': 'Bahan Pengemasan',
			'tarif': 'Tarif Pengemasan'
		}