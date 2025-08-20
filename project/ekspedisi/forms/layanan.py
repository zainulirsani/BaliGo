from django import forms
from ..models import *

class LayananForm(forms.ModelForm):
	class Meta:
		model = Layanan
		fields = ['nama_layanan', 'estimasi_layanan', 'deskripsi', 'publish_status']

		widgets = {
			'nama_layanan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Nama Layanan'}),
			'estimasi_layanan': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tentukan Estimasi Layanan', 'step':'0.01'}),
			'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows' : 6,'placeholder': 'Masukan Deskripsi Layanan'}),
			'publish_status': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px'}),

		}

		labels = {
			'nama_layanan': 'Nama Layanan',
			'no_tlp': 'Estimasi (hari)',
			'deskripsi': 'Deskripsi Layanan',
			'publish_status' : 'Aktifkan'
		}