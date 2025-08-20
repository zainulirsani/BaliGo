from django import forms
from ..models import *

class PersonilForm(forms.ModelForm) :
	def __init__(self, *args, **kwargs) :
		super(PersonilForm, self).__init__(*args, **kwargs)
		self.fields['role'].choices = [
			('', '----------'),
			('adm_gudang', "Admin Gudang"),
			('adm_outlet', "Admin Outlet")
		]
		self.fields['penempatan_toko'].choices = [('', "Pilih Outlet")]
		self.fields['penempatan_gudang'].choices = [('', "Pilih Gudang")]
		
	re_password = forms.CharField(label="Ulangi Password", max_length=100, widget=forms.PasswordInput(
				attrs={'required':True, 'id':'re_password', 'name':'re_password', 'class':"form-control", 'placeholder':"Masukkan ulang password"}))
	class Meta :
		model = User
		fields = ['no_personil', 'first_name', 'email', 'no_telp', 'alamat', 'username', 'role', 'penempatan_toko', 'penempatan_gudang', 'password', 'photo']
		widgets = {
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Masukkan Nama Anda', 'required':True}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Masukkan Email Anda'}),
			'no_telp' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sertakan No Telp Anda (08xxxxxxxx)'}),
			'alamat' : forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Masukkan Alamat Anda', 'rows':4}),
			'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tentukan Username Anda'}),
			'password' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Tentukan Password Anda'}),
			'role' : forms.Select(attrs={'class':'form-control', 'placeholder':'Pilih Jabatan', 'required':True}),
			'penempatan_toko' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Outlet'}),
			'penempatan_gudang' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Gudang'}),

		}
		labels = {
			'first_name' : 'Nama',
			'email' : 'Email',
			'no_telp' : 'Nomor Telp Aktif',
			'alamat' : 'Alamat',
			'username' : 'Username',
			'role' : 'Jabatan',
			'password' : 'Password',
			'penempatan_toko' : 'Penempatan Outlet',
			'penempatan_gudang' : 'Penempatan Gudang'
		}

	def clean(self, *args, **kwargs) :
		password = str(self.cleaned_data.get('password', ''))
		re_password = str(self.cleaned_data.get('re_password', ''))
		if password and re_password and not password.strip() == re_password.strip() :
			raise forms.ValidationError('Password Tidak sama, silahkan ulangi')

	def __init__(self, *args, **kwargs) :
		super(PersonilForm, self).__init__(*args, **kwargs)
		self.fields['role'].choices = [
			('', '----------'),
			('adm_gudang', "Admin Gudang"),
			('adm_outlet', "Admin Outlet")
		]
		self.fields['penempatan_toko'].choices = [('', "Pilih Outlet")]
		self.fields['penempatan_gudang'].choices = [('', "Pilih Gudang")]

class PersonilEditForm(forms.ModelForm) :
	def __init__(self, *args, **kwargs) :
		super(PersonilEditForm, self).__init__(*args, **kwargs)
		self.fields['role'].choices = [
			('', '----------'),
			('adm_gudang', "Admin Gudang"),
			('adm_outlet', "Admin Outlet")
		]
		self.fields['penempatan_toko'].choices = [('', "Pilih Outlet")]
		self.fields['penempatan_gudang'].choices = [('', "Pilih Gudang")]

	password = forms.CharField(label="Password", required=False, max_length=100, widget=forms.PasswordInput(
				attrs={'id':'id_password', 'name':'password', 'class':"form-control", 'placeholder':"Masukkan Password"}))
	re_password = forms.CharField(label="Ulangi Password", required=False, max_length=100, widget=forms.PasswordInput(
				attrs={'id':'re_password', 'name':'re_password', 'class':"form-control", 'placeholder':"Masukkan ulang password"}))
	class Meta :
		model = User
		fields = ['no_personil', 'first_name', 'email', 'no_telp', 'alamat', 'username', 'role', 'penempatan_toko', 'penempatan_gudang', 'photo']
		widgets = {
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Masukkan Nama Anda', 'required':True}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Masukkan Email Anda'}),
			'no_telp' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sertakan No Telp Anda (08xxxxxxxx)'}),
			'alamat' : forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Masukkan Alamat Anda', 'rows':4}),
			'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tentukan Username Anda'}),
			'password' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Tentukan Password Anda','required':False}),
			'role' : forms.Select(attrs={'class':'form-control', 'placeholder':'Pilih Jabatan', 'required':True}),
			'penempatan_toko' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Outlet'}),
			'penempatan_gudang' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Gudang'}),

		}
		labels = {
			'first_name' : 'Nama',
			'email' : 'Email',
			'no_telp' : 'Nomor Telp Aktif',
			'alamat' : 'Alamat',
			'username' : 'Username',
			'role' : 'Jabatan',
			'password' : 'Password',
			'penempatan_toko' : 'Penempatan Outlet',
			'penempatan_gudang' : 'Penempatan Gudang'
		}

	def clean(self, *args, **kwargs) :
		password = str(self.cleaned_data.get('password', ''))
		re_password = str(self.cleaned_data.get('re_password', ''))
		if password :
			if re_password :
				if not password.strip() == re_password.strip() :
					raise forms.ValidationError('Password Tidak sama, silahkan ulangi')
			else :
				raise forms.ValidationError('Silahkan isi ulangi password, tidak boleh kosong')



class PersonilEditFormV2(forms.ModelForm) :

	def __init__(self, *args, **kwargs) :
		super(PersonilEditFormV2, self).__init__(*args, **kwargs)
		self.fields['role'].choices = [
			('', '----------'),
			('adm_gudang', "Admin Gudang"),
			('adm_outlet', "Admin Outlet")
		]
		self.fields['penempatan_toko'].choices = [('', "Pilih Outlet")]
		self.fields['penempatan_gudang'].choices = [('', "Pilih Gudang")]

	class Meta :
		model = User
		fields = ['first_name', 'no_telp', 'alamat', 'role', 'penempatan_toko', 'penempatan_gudang', 'photo']
		widgets = {
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Masukkan Nama Anda', 'required':True}),
			'no_telp' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sertakan No Telp Anda (08xxxxxxxx)'}),
			'alamat' : forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Masukkan Alamat Anda', 'rows':4}),
			'role' : forms.Select(attrs={'class':'form-control', 'placeholder':'Pilih Jabatan', 'required':True}),
			'penempatan_toko' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Outlet'}),
			'penempatan_gudang' : forms.Select(attrs={'class':'form-control hidden', 'placeholder':'Pilih Gudang'}),

		}
		labels = {
			'first_name' : 'Nama',
			'no_telp' : 'Nomor Telp Aktif',
			'alamat' : 'Alamat',
			'role' : 'Jabatan',
			'penempatan_toko' : 'Penempatan Outlet',
			'penempatan_gudang' : 'Penempatan Gudang'
		}

class ProfileUploadPhoto(forms.ModelForm) :
	class Meta :
		model = User
		fields = ['photo']

	