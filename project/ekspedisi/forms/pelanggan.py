from django import forms
from django.db import transaction
from ..models import *
import datetime
from random import randint

class PelangganDetailInfoForm(forms.ModelForm):
	class Meta :
		model = InformasiPelanggan
		fields = ['provinsi', 'kota', 'kecamatan', 'desa', 'kode_pos']

class PelangganForm(forms.ModelForm):
	re_password = forms.CharField(label="Ulangi Password", max_length=100, widget=forms.PasswordInput(
				attrs={'required':True, 'id':'re_password', 'name':'re_password', 'class':"form-control", 'placeholder':"Masukkan ulang password"}))
	class Meta :
		model = User
		fields = ['no_personil', 'first_name', 'email', 'no_telp', 'alamat', 'username', 'password', 'register_sebagai']
		widgets = {
			'no_personil' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'ID Pelanggan', 'readonly':True}),
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Masukkan Nama Anda', 'required':True}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Masukkan Email Anda', 'required':True}),
			'no_telp' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sertakan No Telp Anda (08xxxxxxxx)', 'required':True}),
			'alamat' : forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Masukkan Alamat Anda', 'rows':4, 'required':True}),
			'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tentukan Username Anda', 'required':True}),
			'password' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Tentukan Password Anda', 'required':True}),
			'register_sebagai' : forms.Select(choices=[('personal', 'Personal'),('goverment', 'Goverment'),('company', 'Company'),], attrs={'class':'form-control', 'placeholder':'Pilih Registrasi', 'required':True})
		}
		labels = {
			'no_personil' : 'ID',
			'first_name' : 'Nama',
			'email' : 'Email',
			'no_telp' : 'Nomor Telp Aktif',
			'alamat' : 'Alamat',
			'username' : 'Username',
			'password' : 'Password',
			'register_sebagai' : 'Register Sebagai'
		}
	field_order = [
			'no_personil',
			'first_name',
			'email',
			'no_telp',
			'alamat',
			'username',
			'password',
			're_password',
			'register_sebagai'
		]

	def clean(self, *args, **kwargs) :
		password = str(self.cleaned_data.get('password', ''))
		re_password = str(self.cleaned_data.get('re_password', ''))
		if password and re_password and not password.strip() == re_password.strip() :
			raise forms.ValidationError('Password Tidak sama, silahkan ulangi')

	def __init__(self, *args, **kwargs) :
		super(PelangganForm, self).__init__(*args, **kwargs)
		self.fields['register_sebagai'].choices = [
			('personal', 'Personal'),
			('goverment', 'Goverment'),
			('company', 'Company'),
		]

class PelangganFormEdit(forms.ModelForm):
	class Meta :
		model = User
		fields = ['first_name', 'email', 'no_telp', 'alamat', 'username', 'register_sebagai']
		widgets = {
			'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Masukkan Nama Anda', 'required':True}),
			'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Masukkan Email Anda'}),
			'no_telp' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sertakan No Telp Anda (08xxxxxxxx)'}),
			'alamat' : forms.Textarea(attrs={'class':'form-control', 'placeholder' : 'Masukkan Alamat Anda', 'rows':4}),
			'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Tentukan Username Anda'}),
			'register_sebagai' : forms.Select(choices=[('personal', 'Personal'),('goverment', 'Goverment'),('company', 'Company'),], attrs={'class':'form-control', 'placeholder':'Pilih Registrasi', 'required':True})
		}
		labels = {
			'first_name' : 'Nama',
			'email' : 'Email',
			'no_telp' : 'Nomor Telp Aktif',
			'alamat' : 'Alamat',
			'username' : 'Username',
			'register_sebagai' : 'Register Sebagai'
		}
	field_order = [
			'first_name',
			'email',
			'no_telp',
			'alamat',
			'username',
			'register_sebagai'
		]

	def __init__(self, *args, **kwargs) :
		super(PelangganFormEdit, self).__init__(*args, **kwargs)
		self.fields['register_sebagai'].choices = [
			('personal', 'Personal'),
			('goverment', 'Goverment'),
			('company', 'Company'),
		]