from django import forms
from ..models import *


class SatuanForm(forms.ModelForm):

	class Meta:
		model = Satuan
		fields = ['nama_satuan']

		widgets = {
			'nama_satuan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Satuan', 'required': True})
		}

		labels = {
			'nama_satuan': 'Nama Satuan',
		}