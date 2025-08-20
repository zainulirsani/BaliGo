from django import forms
from ..models import *

class GudangForm(forms.ModelForm):

	def __init__(self, *args, **kwargs) :
		super(GudangForm, self).__init__(*args, **kwargs)
		self.fields['provinsi_gudang'].choices = [('', "--------")]
		self.fields['kota_gudang'].choices = [('', "--------")]
		self.fields['kecamatan_gudang'].choices = [('', "--------")]
		self.fields['desa_gudang'].choices = [('', "--------")]
		self.fields['kode_pos_gudang'].choices = [('', "--------")]

	class Meta:
		model = Gudang
		fields = ['id_gudang', 'nama_gudang', 'no_tlp', 'alamat', 'titik_lokasi', 'radius', 'provinsi_gudang', 'kota_gudang', 'kecamatan_gudang', 'desa_gudang', 'kode_pos_gudang']

		widgets = {
			'id_gudang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan id Gudang', 'id': 'inputId', 'readonly': True}),
			'nama_gudang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Nama Gudang', 'id': 'inputNama', 'required': True}),
			'no_tlp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan No Tlp', 'id': 'inputNoTlp', 'required': True}),
			'alamat': forms.Textarea(attrs={'class': 'form-control','rows': '3','placeholder': 'Masukan Alamat Gudang', 'id': 'inputAlamat', 'required': True}),
			'titik_lokasi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Koordinat dengan klik lokasi pada peta', 'id': 'inputTitikLokasi', 'readonly': True, 'required': True}),
			'radius': forms.TextInput(attrs={'class': 'form-control', 'id': 'radius'}),

			'provinsi_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Provinsi Gudang', 'id': 'inputProvinsiGudang'}), 
			'kota_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kab/Kota Gudang', 'id': 'inputKotaGudang'}),
			'kecamatan_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kecamatan Gudang', 'id': 'inputKecamatanGudang'}),
			'desa_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Desa Gudang', 'id': 'inputDesaGudang'}),
			'kode_pos_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kode Pos Gudang', 'id': 'inputKodePosGudang'}),
		}

		labels = {
            'id_gudang': 'ID Gudang',
            'nama_gudang': 'Nama Gudang',
            'no_tlp': 'NO. Tlp',
            'alamat': 'Alamat',
            'titik_lokasi': 'Titik Lokasi',
            'radius': 'Radius Scan',
            'provinsi_gudang': 'Provinsi',
            'kota_gudang': 'Kota/Kabupaten',
            'kecamatan_gudang': 'Kecamatan',
            'desa_gudang': 'Desa',
            'kode_pos_gudang': 'Kode POS',
        }