from django import forms
from ..models import *

# REVISI LABEL:
# Label Detail Barang => Isi Kiriman

class PengirimanForm(forms.ModelForm):

	def __init__(self, *args, **kwargs) :
		super(PengirimanForm, self).__init__(*args, **kwargs)
		self.fields['pengemasan'].queryset = Pengemasan.objects.filter(is_active=True)
		
		# Berfungsi agar tidak meload data atau record dari model yg terforeign key (agar tidak berat saat meload template dengan form ini)
		self.fields['provinsi_pengirim'].choices = [('', "--------")]
		self.fields['outlet_pengiriman'].choices = [('', "--------")]
		self.fields['gudang_pengiriman'].choices = [('', "--------")]
		self.fields['kota_pengirim'].choices = [('', "--------")]
		self.fields['kecamatan_pengirim'].choices = [('', "--------")]
		self.fields['desa_pengirim'].choices = [('', "--------")]
		self.fields['kode_pos_pengirim'].choices = [('', "--------")]
		self.fields['provinsi_penerima'].choices = [('', "--------")]
		self.fields['kota_penerima'].choices = [('', "--------")]
		self.fields['kecamatan_penerima'].choices = [('', "--------")]
		self.fields['desa_penerima'].choices = [('', "--------")]
		self.fields['kode_pos_penerima'].choices = [('', "--------")]
		self.fields['outlet_penerimaan'].choices = [('', "--------")]
		self.fields['gudang_penerimaan'].choices = [('', "--------")]
		self.fields['pengemasan'].choices = [('', "Tidak Memerlukan Pengemasan Lagi")]
		self.fields['layanan'].choices = [('', "----------")]
		self.fields['satuan'].choices = [('', "Pilih Satuan")]
		self.fields['satuan'].required = False
		self.fields['pengemasan'].required = False
 
	class Meta:
		model = Pengiriman
		fields = [
			'id_pengiriman', 
			'outlet_pengiriman',
			'gudang_pengiriman', 
			'nama_pengirim', 
			'status_pengirim', 
			'no_telp_pengirim', 
			# 'email_pengirim', 
			'alamat_pengirim', 
			
			'provinsi_pengirim',
			'kota_pengirim', 
			'kecamatan_pengirim',
			'desa_pengirim',
			'kode_pos_pengirim',
			
			'nama_penerima',
			'no_telp_penerima',
			# 'email_penerima',
			'alamat_penerima',
			
			'provinsi_penerima',
			'kota_penerima',
			'kecamatan_penerima',
			'desa_penerima',
			'kode_pos_penerima',
			
			'outlet_penerimaan',
			'gudang_penerimaan',
			'jenis_barang',
			'detail_barang',
			'pengemasan',
			'layanan',
			'berat',
			'jumlah',
			'satuan',
			'pencatat',
			'tarif_berat',
			'tarif_kilometer',
			'tarif_gudang',
			'tarif_layanan',
			'tarif_pengemasan',
			'tarif_lain',
			'total_tarif',
			'extra_tarif_pengirim',
			'extra_tarif_penerima',
			'keterangan_extra_tarif'
		]

		

		widgets = {
			'outlet_pengiriman': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Outlet Pengiriman', 'id': 'inputOutletPengiriman'}), 
			'gudang_pengiriman': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gudang Pengiriman', 'id': 'inputGudangPengiriman'}), 
			'status_pengirim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Status Pengirim', 'id': 'inputStatusPengirim'}), 
			'nama_pengirim': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nama Pengirim', 'id': 'inputNamaPengirim', 'rows':3}), 
			'no_telp_pengirim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Tlp. Pengirim', 'id': 'inputNoTlpPengirim'}), 
			# 'email_pengirim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Pengirim', 'id': 'inputEmailPengirim'}), 
			'alamat_pengirim': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat Pengirim', 'id': 'inputAlamatPengirim', 'rows':3}), 
			
			'provinsi_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Provinsi Pengirim', 'id': 'inputProvinsiPengirim'}), 
			'kota_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kab/Kota Pengirim', 'id': 'inputKotaPengirim'}),
			'kecamatan_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kecamatan Pengirim', 'id': 'inputKecamatanPengirim'}),
			'desa_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Desa Pengirim', 'id': 'inputDesaPengirim'}),
			'kode_pos_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kode Pos Pengirim', 'id': 'inputKodePosPengirim'}),
			
			'nama_penerima': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nama Penerima', 'id': 'inputNamaPenerima', 'rows':3}),
			'no_telp_penerima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Tlp. Penerima', 'id': 'inputNoTlpPenerima'}),
			# 'email_penerima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Penerima', 'id': 'inputEmailPenerima'}),
			'alamat_penerima': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat Penerima', 'id': 'inputAlamatPenerima', 'rows':3}),
			
			'provinsi_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Provinsi Penerima', 'id': 'inputProvinsiPenerima'}),
			'kota_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kab/Kota Penerima', 'id': 'inputKotaPenerima'}),
			'kecamatan_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kecamatan Penerima', 'id': 'inputKecamatanPenerima'}),
			'desa_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Desa Penerima', 'id': 'inputDesaPenerima'}),
			'kode_pos_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Kode Pos Penerima', 'id': 'inputKodePosPenerima'}),
			
			'outlet_penerimaan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Outlet Penerimaan', 'id': 'inputOutletPenerimaan'}),
			'gudang_penerimaan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Gudang Penerimaan', 'id': 'inputGudangPenerimaan'}),
			'jenis_barang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Jenis Barang', 'id': 'inputJenisBarang', 'required': 'required'}),
			'detail_barang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Isi Kiriman (Detail Kiriman)', 'id': 'inputDetailBarang', 'required': 'required'}),
			'pengemasan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Tidak Memerlukan Pengemasan Lagi', 'id': 'inputPengemasan'}),
			'layanan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Layanan', 'id': 'inputLayanan'}),
			'berat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan berat Barang (Kg)', 'id': 'inputBerat'}),
			'jumlah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Jumlah Barang', 'id': 'inputJumlah', 'type': 'number'}),
			'satuan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Satuan', 'id': 'inputSatuan'}),
			'pencatat': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pencatat / Admin Toko', 'id': 'inputAdminToko', 'readonly': True}),
			'tarif_berat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif berat', 'id': 'inputTarifberat', 'readonly': True}),
			'tarif_kilometer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif Kilometer', 'id': 'inputTarifKilometer', 'readonly': True}),
			'tarif_gudang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif Gudang', 'id': 'inputTarifGudang', 'readonly': True}),
			'tarif_layanan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif Layanan', 'id': 'inputTarifLayanan', 'readonly': True}),
			'total_tarif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Tarif', 'id': 'inputTotalTarif', 'readonly': True}),
			'extra_tarif_pengirim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Extra Tarif Pengirim', 'id': 'inputExtraTarifPengirim', 'readonly': True}),
			'extra_tarif_penerima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Extra Tarif Penerima', 'id': 'inputExtraTarifPenerima', 'readonly': True}),
			'keterangan_extra_tarif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keterangan Extra Tarif', 'id': 'inputKeteranganExtraTarif', 'readonly': True}),
		}

		labels = {
			'status_pengirim': 'Status Pengirim',
			'outlet_pengiriman' : 'Outlet Pengirim', 
			'gudang_pengiriman' : 'Gudang Pengirim', 
			'nama_pengirim': 'Nama Pengirim', 
			'no_telp_pengirim': 'No. Tlp. Pengirim', 
			'email_pengirim': 'Email Pengirim', 
			'alamat_pengirim': 'Alamat Pengirim', 
			
			'provinsi_pengirim': 'Provinsi Pengirim',
			'kota_pengirim': 'Kab/Kota Pengirim', 
			'kecamatan_pengirim': 'Kecamatan Pengirim',
			'desa_pengirim': 'Desa Pengirim',
			'kode_pos_pengirim': 'Kode Pos Pengirim',
			
			'nama_penerima': 'Nama Penerima',
			'no_telp_penerima': 'No. Tlp. Penerima',
			'email_penerima': 'Email Penerima',
			'alamat_penerima': 'Alamat Penerima',
			
			'provinsi_penerima': 'Provinsi Penerima',
			'kota_penerima': 'Kab/Kota Penerima',
			'kecamatan_penerima': 'Kecamatan Penerima',
			'desa_penerima': 'Desa Penerima',
			'kode_pos_penerima': 'Kode Pos Penerima',
			
			'outlet_penerimaan': 'Outlet Penerima',
			'gudang_penerimaan': 'Gudang Penerima',
			'jenis_barang': 'Jenis Barang',
			'detail_barang': 'Isi Kiriman',
			'pengemasan': 'Pengemasan',
			'layanan': 'Layanan',
			'berat': 'Berat Barang',
			'jumlah': 'Jumlah',
			'satuan': 'Satuan',
			'pencatat': 'Pencatat',
			'tarif_berat': 'Tarif berat',
			'tarif_kilometer': 'Tarif Kilometer',
			'tarif_gudang': 'Tarif Gudang',
			'tarif_layanan': 'Tarif Layanan',
			'total_tarif': 'Total Tarif',
			'tarif_lain': 'Tarif Lain - Lain',
			'extra_tarif_pengirim': 'Extra Tarif Pengirim',
			'extra_tarif_penerima': 'Extra Tarif Penerima',
			'keterangan_extra_tarif': 'Keterangan Extra Tarif',
		}

	