from django import forms
from ..models import *

class KendaraanForm(forms.ModelForm):
	class Meta:
		model = Kendaraan
		fields = ['id_kendaraan','nama_kendaraan', 'no_kendaraan', 'jenis_kendaraan', 'penempatan_toko', 'penempatan_gudang', 'kapasitas_tank', 'bahan_bakar']

		widgets = {
			'nama_kendaraan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Nama Kendaraan', 'id': 'inputNama'}),
			'no_kendaraan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan No Plat Kendaraan', 'id': 'inputNo'}),
			'jenis_kendaraan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Jenis Kendaraan', 'id': 'inputJenisKendaraan'}),
			'penempatan_toko': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Penempatan Toko', 'id': 'inputToko'}),
			'penempatan_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Penempatan Gudang', 'id': 'inputGudang'}),
			'kapasitas_tank': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Kapasistas Tank (liter)', 'id': 'inputKapasitas'}),
			'bahan_bakar': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Jenis Bahan Bakar', 'id': 'inputBahanBakar'})
		}

		labels = {
			'nama_kendaraan': 'Nama Kendaraan',
			'no_kendaraan': 'No Plat',
			'jenis_kendaraan': 'Jenis',
			'penempatan_toko': 'Penempatan Toko',
			'penempatan_gudang': 'Penempatan Gudang',
			'kapasitas_tank': 'Kapasitas Tank',
			'bahan_bakar': 'Bahan Bakar'
		}
	def __init__(self, *args, **kwargs) :
		super(KendaraanForm, self).__init__(*args, **kwargs)
		self.fields['penempatan_toko'].choices = [('', "Pilih Outlet")]
		self.fields['penempatan_gudang'].choices = [('', "Pilih Gudang")]