from django import forms
from ..models import *


class LogPengirimanForm(forms.ModelForm):

	def __init__(self, *args, **kwargs) :
		super(LogPengirimanForm, self).__init__(*args, **kwargs)
		
		# Berfungsi agar tidak meload data atau record dari model yg terforeign key (agar tidak berat saat meload template dengan form ini)
		self.fields['id_pengiriman'].choices = [('', "--------")]
		self.fields['rute_pengiriman_outlet'].choices = [('', "--------")]
		self.fields['rute_pengiriman_gudang'].choices = [('', "--------")]
		self.fields['rute_pengiriman_gudang_akhir'].choices = [('', "--------")]
		self.fields['rute_pengiriman_outlet_akhir'].choices = [('', "--------")]
		self.fields['id_kurir'].choices = [('', "--------")]

	class Meta:
		model = LogPengiriman
		fields = ['id_pengiriman', 'rute_pengiriman_outlet', 'rute_pengiriman_gudang', 'rute_pengiriman_gudang_akhir', 'rute_pengiriman_outlet_akhir', 'titik_lokasi', 'id_kurir', 'status_pengiriman']

		widgets = {
			'titik_lokasi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Nama Layanan'}),
			'status_pengiriman': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tentukan Estimasi Layanan', 'step':'0.01'}),
		}

		labels = {
			'titik_lokasi': 'Titik Lokasi',
			'status_pengiriman': 'Status Pengiriman',
		}