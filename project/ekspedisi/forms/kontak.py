from django import forms
from ..models import *

class KontakForm(forms.ModelForm):
	class Meta:
		model = Kontak
		fields = ['alamat', 'no_tlp', 'email']

		widgets = {
			'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': '6', 'placeholder': 'Masukan Alamat', 'id': 'inputAlamat'}),
			'no_tlp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan No.Tlp', 'id': 'inputNoTlp'}),
			'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Email', 'id': 'inputEmail'}),
		}

		labels = {
			'alamat': 'Alamat',
			'no_tlp': 'No. Tlp',
			'email': 'Email',
		}