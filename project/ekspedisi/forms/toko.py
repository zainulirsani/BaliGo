from django import forms
from ..models import *

class TokoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	# first call parent's constructor
		super(TokoForm, self).__init__(*args, **kwargs)
		# there's a `fields` property now
		self.fields['kontak'].required = True
		self.fields['id_toko'].required = True
		self.fields['nama_toko'].required = True
		self.fields['alamat'].required = True
		self.fields['provinsi_toko'].choices = [('', "--------")]
		self.fields['kota_toko'].choices = [('', "--------")]
		self.fields['kecamatan_toko'].choices = [('', "--------")]
		self.fields['desa_toko'].choices = [('', "--------")]
		self.fields['kode_pos_toko'].choices = [('', "--------")]


	class Meta:
		model = Toko
		fields = ['id_toko', 'nama_toko', 'alamat', 'kontak', 'titik_lokasi', 'radius', 'provinsi_toko', 'kota_toko', 'kecamatan_toko', 'desa_toko', 'kode_pos_toko']

		widgets = {
			'id_toko': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan ID Outlet', 'id': 'inputId', 'readonly': True}),
			'nama_toko': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Nama Outlet', 'id': 'inputNama', 'required': True}),
			'alamat': forms.Textarea(attrs={'class': 'form-control','rows': '3','placeholder': 'Masukan Alamat Outlet', 'id': 'inputAlamat', 'required': True}),
			'kontak': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan No Tlp', 'id': 'inputNoTlp','required': True}),
			'titik_lokasi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Koordinat dengan klik lokasi pada peta', 'id': 'inputTitikLokasi', 'readonly': True, 'required': True}),
			'radius': forms.TextInput(attrs={'class': 'form-control', 'id': 'radius'}),

			'provinsi_toko': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Provinsi Outlet', 'id': 'inputProvinsiToko'}), 
			'kota_toko': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kab/Kota Outlet', 'id': 'inputKotaToko'}),
			'kecamatan_toko': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kecamatan Outlet', 'id': 'inputKecamatanToko'}),
			'desa_toko': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Desa Outlet', 'id': 'inputDesaToko'}),
			'kode_pos_toko': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kode Pos Outlet', 'id': 'inputKodePosToko'}),
		}

		labels = {
            'id_toko': 'ID Outlet',
            'nama_toko': 'Nama Outlet',
            'alamat': 'Alamat',
            'kontak': 'No. Tlp',
            'titik_lokasi': 'Titik Lokasi',
            'radius': 'Radius Scan',
            'provinsi_toko': 'Provinsi',
            'kota_toko': 'Kota/Kabupaten',
            'kecamatan_toko': 'Kecamatan',
            'desa_toko': 'Desa',
            'kode_pos_toko': 'Kode POS',

        }