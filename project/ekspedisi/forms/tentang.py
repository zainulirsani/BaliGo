from django import forms
from ..models import *

class TentangForm(forms.ModelForm):
	class Meta:
		model = Tentang
		fields = ['deskripsi']

		widgets = {
			'deskripsi': forms.Textarea(attrs={'class': 'form-control','rows': '6','placeholder': 'Masukan Data Deskripsi', 'id': 'inputDeskripsi'}),
		}

		labels = {
            'deskripsi': 'Deskripsi',
        }