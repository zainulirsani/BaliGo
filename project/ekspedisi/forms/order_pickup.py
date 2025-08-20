from django import forms
from ..models import *

STATUS_CHOICES= [
	('approve', 'Approve'),
	('pickup', 'Pick Up'),
	('done', 'Done')
	]
class OrderPickupForm(forms.ModelForm):
	class Meta:
		model = OrderPickup
		fields = [
			'id_order', 
			'id_customer', 
			'jenis_barang', 
			'detail_barang', 
			'jenis_pengiriman', 
			'id_pengemasan',
			'nama_penerima',
			'no_tlp_penerima',
			'email_penerima',
			'alamat_penerima', 
			'id_toko',
			'id_gudang', 
			'status'
		]

		widgets = {
			'id_order': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputId'}),
			'id_customer': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputIdCustomer'}),
			'jenis_barang': forms.Select(attrs={'class': 'form-control', 'id': 'inputJenisBarang'}),
			'detail_barang': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputDetailBarang'}),
			'jenis_pengiriman': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputJenisPengiriman'}),
			'id_pengemasan': forms.Select(attrs={'class': 'form-control', 'id': 'inputIdPengemasan'}),
			'nama_penerima': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputNamaPenerima'}),
			'no_tlp_penerima': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputNoTlpPenerima'}),
			'email_penerima': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputEmailPenerima'}),
			'alamat_penerima': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputAlamatPenerima'}),
			'id_toko': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputIdToko'}),
			'id_gudang': forms.TextInput(attrs={'class': 'form-control', 'id': 'inputIdGudang'}),
			'status': forms.Select(choices=STATUS_CHOICES, attrs={'class':'form-control','id': 'inputRegister', 'placeholder': 'Pilih Status'}),
		}

		labels = {
			'id_order' : 'Id Order', 
			'id_customer' : 'Id Pelanggan', 
			'jenis_barang': 'Jenis Barang', 
			'detail_barang': 'Detail Barang', 
			'jenis_pengiriman': 'Jenis Pengiriman', 
			'id_pengemasan': 'Jenis Pengemasan', 
			'nama_penerima': 'Nama Penerima',
			'no_tlp_penerima': 'No. Tlp. Penerima',
			'email_penerima': 'Email Penerima',
			'alamat_penerima': 'Alamat Penerima',
			'id_toko': 'Id Toko',
			'id_toko': 'Id Gudang',  
			'status': 'Status',
		}


class PelangganOrderPickupForm(forms.ModelForm):
	def __init__(self, *args, **kwargs) :
		super(PelangganOrderPickupForm, self).__init__(*args, **kwargs)
		self.fields['id_pengemasan'].queryset = Pengemasan.objects.filter(is_active=True)
		
		# Berfungsi agar tidak meload data atau record dari model yg terforeign key (agar tidak berat saat meload template dengan form ini)
		self.fields['provinsi_pengirim'].choices = [('', "Pilih Provinsi Pengirim")]
		self.fields['id_toko'].choices = [('', "--------")]
		self.fields['id_toko2'].choices = [('', "--------")]
		self.fields['kota_pengirim'].choices = [('', "Pilih Kota/Kab. Pengirim")]
		self.fields['kecamatan_pengirim'].choices = [('', "Pilih Kec. Pengirim")]
		self.fields['desa_pengirim'].choices = [('', "Pilih Desa/Kelurahan Pengirim")]
		self.fields['kode_pos_pengirim'].choices = [('', "Kode Pos Pengirim")]
		self.fields['provinsi_penerima'].choices = [('', "Pilih Provinsi Penerima")]
		self.fields['kota_penerima'].choices = [('', "Pilih Kota/Kab. Penerima")]
		self.fields['kecamatan_penerima'].choices = [('', "Pilih Kec. Penerima")]
		self.fields['desa_penerima'].choices = [('', "Pilih Desa/Kelurahan Penerima")]
		self.fields['kode_pos_penerima'].choices = [('', "Kode Pos Penerima")]
		self.fields['id_pengemasan'].choices = [('', "Tidak Perlu Pengemasan Lagi")]
		self.fields['id_gudang'].choices = [('', "---------")]
		self.fields['id_gudang2'].choices = [('', "---------")]
		self.fields['jenis_pengiriman'].choices = [('', "---------")]
		self.fields['satuan'].choices = [('', "Pilih Satuan")]

	class Meta:
		model = OrderPickup
		fields = [
			'status_pengirim',
			'id_order',
			'id_customer',
			'id_toko',
			'id_gudang',
			'id_toko2',
			'id_gudang2',
			
			'provinsi_pengirim',
			'kota_pengirim', 
			'kecamatan_pengirim',
			'desa_pengirim',
			'kode_pos_pengirim',
			
			'nama_penerima',
			'no_tlp_penerima',
			'email_penerima',
			'alamat_penerima',
			
			'provinsi_penerima',
			'kota_penerima',
			'kecamatan_penerima',
			'desa_penerima',
			'kode_pos_penerima',
			
			'keterangan_cancel',

			'jenis_barang',
			'detail_barang',
			'id_pengemasan',
			'jenis_pengiriman',
			'status',
			'jumlah',
			'satuan',

			'berat',
			'tarif_berat',
			'tarif_kilometer',
			'tarif_gudang',
			'tarif_layanan',
			'extra_tarif_pengirim',
			'extra_tarif_penerima',
			'total_tarif',
			'keterangan_extra_tarif'
			]


		widgets = {

			'id_order': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Id Order',}),
			'id_customer': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Input Id Customer', 'required': True}),
			'id_toko': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Input Id Outlet', 'required': True}),
			'id_gudang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Input Id Gudang', 'required': True}),
			
			'provinsi_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Provinsi', 'required': True}),
			'kota_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kota/Kabupaten', 'required': True}), 
			'kecamatan_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kecamatan', 'required': True}),
			'desa_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Desa/Kelurahan', 'required': True}),
			'kode_pos_pengirim': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kode Pos', 'required': True}),
			
			'nama_penerima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Penerima', 'required': True}),
			'no_tlp_penerima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Tlp. Penerima', 'required': True,}),
			'email_penerima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email (Example@gmail.com)',}),
			'alamat_penerima': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Alamat Penerima', 'rows':4, 'required': True}),
			
			'provinsi_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Provinsi', 'required': True}),
			'kota_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kota/Kabupaten', 'required': True}),
			'kecamatan_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kecamatan', 'required': True}),
			'desa_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Desa/Kelurahan', 'required': True}),
			'kode_pos_penerima': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Kode Pos', 'required': True}),
			
			'keterangan_cancel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Keterangan Cancel',}),

			'jenis_barang': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Jenis Barang', 'required': True}),
			'detail_barang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Detail Barang',}),
			'id_pengemasan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Pengemasan',}),
			'jenis_pengiriman': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Jenis Pengiriman', 'required': True}),
			'status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Status',}),
			'jumlah': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Jumlah Barang', 'id': 'inputJumlah', 'type': 'number'}),
			'satuan': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pilih Satuan', 'id': 'inputSatuan'}),

			'berat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input Berat (Kg)', 'required': True}),
			'tarif_berat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif Berat', 'readonly': True, 'type': 'hidden'}),
			'tarif_kilometer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif Kilometer', 'readonly': True, 'type': 'hidden'}),
			'tarif_gudang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif Gudang', 'readonly': True, 'type': 'hidden'}),
			'tarif_layanan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tarif Layanan', 'readonly': True, 'type': 'hidden'}),
			'extra_tarif_pengirim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Extra Tarif Pengirim', 'readonly': True, 'type': 'hidden'}),
			'extra_tarif_penerima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Extra Tarif Penerima', 'readonly': True, 'type': 'hidden'}),
			'total_tarif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Tarif', 'readonly': True, 'type': 'hidden'}),
			'keterangan_extra_tarif': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keterangan Extra Tarif', 'readonly': True, 'type': 'hidden'}),
		}

		labels = {
			'id_order' : 'ID Order',
			'id_customer': 'Pengirim',
			'id_toko': 'Outlet Terdekat',
			'id_gudang': 'Gudang Terdekat',
			
			'provinsi_pengirim': 'Provinsi Pengirim',
			'kota_pengirim': 'Kota Pengirim', 
			'kecamatan_pengirim': 'Kec. Pengirim',
			'desa_pengirim': 'Desa Pengirim',
			'kode_pos_pengirim': 'Kode Pos Pengirim',
			
			'nama_penerima': 'Nama Penerima',
			'no_tlp_penerima': 'No. Tlp. Penerima',
			'email_penerima': 'Email Penerima',
			'alamat_penerima': 'Alamat Penerima',
			
			'provinsi_penerima': 'Provinsi Penerima',
			'kota_penerima': 'Kota Penerima',
			'kecamatan_penerima': 'Kec. Penerima',
			'desa_penerima': 'Desa Penerima',
			'kode_pos_penerima': 'Kode Pos Penerima',
			
			'keterangan_cancel': 'Keterangan Cancel',

			'jenis_barang': 'Jenis Barang',
			'detail_barang': 'Detail Barang',
			'id_pengemasan': 'Pengemasan',
			'jenis_pengiriman': 'Jenis Pengiriman',
			'status': 'Status Pengiriman',

			'berat': 'Berat Total (Kg)',
			'jumlah': 'Jumlah Barang',
			'satuan': 'Satuan',
			'tarif_berat': 'Tarif Berat',
			'tarif_kilometer': 'Tarif Kilometer',
			'tarif_gudang': 'Tarif Gudang',
			'tarif_layanan': 'Tarif Layanan',
			'extra_tarif_pengirim': 'Extra Tarif Pengirim',
			'extra_tarif_penerima': 'Extra Tarif Penerima',
			'total_tarif': 'Total',
			'keterangan_extra_tarif': 'Keterangan Extra Tarif',
		}