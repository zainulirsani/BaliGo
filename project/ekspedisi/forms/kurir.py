from django import forms
from ..models import *

class KurirForm(forms.ModelForm) :
	re_password = forms.CharField(label="Ulangi Password", max_length=100, widget=forms.PasswordInput(
				attrs={'id':'re_password', 'name':'re_password', 'class':"form-control", 'placeholder':"Masukkan ulang password"}))
	class Meta :
		model = User
		fields = ['no_personil', 'first_name', 'email', 'no_telp', 'alamat', 'username', 'role', 'penempatan_toko', 'penempatan_gudang', 'password', 'photo']
		widgets = {
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Masukkan Nama Anda', 'id': 'inputNama', 'required': True}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Masukkan Email Anda', 'id': 'inputEmail'}),
			'no_telp' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sertakan No Telp Anda (08xxxxxxxx)', 'id': 'inputNoTlp'}),
			'alamat' : forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Masukkan Alamat Anda', 'rows':4, 'id': 'inputAlamat'}),
			'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tentukan Username Anda', 'id': 'inputUsername'}),
			'password' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Tentukan Password Anda', 'id': 'inputPassword'}),
			'role' : forms.Select(attrs={'class':'form-control', 'placeholder':'Pilih Jabatan', 'id': 'inputRole', 'readonly': True}),
			'penempatan_toko' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Outlet', 'id': 'inputToko'}),
			'penempatan_gudang' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Gudang', 'id': 'inputGudang'}),

		}
		labels = {
			'first_name' : 'Nama',
			'email' : 'Email',
			'no_telp' : 'Nomor Telp Aktif',
			'alamat' : 'Alamat',
			'username' : 'Username',
			'password' : 'Password',
			'role' : 'Jabatan',
			'penempatan_toko' : 'Penempatan Outlet',
			'penempatan_gudang' : 'Penempatan Gudang'
		}

	def clean(self, *args, **kwargs) :
		password = str(self.cleaned_data.get('password', ''))
		re_password = str(self.cleaned_data.get('re_password', ''))
		if password and re_password and not password.strip() == re_password.strip() :
			raise forms.ValidationError('Password Tidak sama, silahkan ulangi')

	def __init__(self, *args, **kwargs) :
		super(KurirForm, self).__init__(*args, **kwargs)
		self.fields['role'].choices = [
			('kurir', "Kurir")
		]
		self.fields['penempatan_toko'].choices = [('', "Pilih Outlet")]
		self.fields['penempatan_gudang'].choices = [('', "Pilih Gudang")]


class KurirFormEdit(forms.ModelForm) :
	class Meta :
		model = User
		fields = ['first_name', 'no_telp', 'alamat', 'penempatan_toko', 'penempatan_gudang', 'photo']
		widgets = {
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Masukkan Nama Anda', 'id': 'inputNama'}),
			'no_telp' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sertakan No Telp Anda (08xxxxxxxx)', 'id': 'inputNoTlp'}),
			'alamat' : forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Masukkan Alamat Anda', 'rows':4, 'id': 'inputAlamat'}),
			'penempatan_toko' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Outlet', 'id': 'inputToko'}),
			'penempatan_gudang' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Gudang', 'id': 'inputGudang'}),

		}
		labels = {
			'first_name' : 'Nama',
			'no_telp' : 'Nomor Telp Aktif',
			'alamat' : 'Alamat',
			'penempatan_toko' : 'Penempatan Outlet',
			'penempatan_gudang' : 'Penempatan Gudang'
		}

	def __init__(self, *args, **kwargs) :
		super(KurirFormEdit, self).__init__(*args, **kwargs)
		self.fields['penempatan_toko'].choices = [('', "Pilih Outlet")]
		self.fields['penempatan_gudang'].choices = [('', "Pilih Gudang")]

class KurirTTD(forms.ModelForm) :
	class Meta :
		model = TandaTerima
		fields = ['id_pengiriman','nama_penerima', 'keterangan']

class KurirTTDBuktiFoto(forms.ModelForm) :
	class Meta :
		model = BuktiFotoTandaTerima
		fields = ['id_ttd','foto']