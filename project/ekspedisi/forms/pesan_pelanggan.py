from django import forms
from ..models import *

class PesanPelangganForm(forms.ModelForm):
	class Meta:
		model = PesanPelanggan
		fields = ['nama', 'email', 'no_hp', 'judul', 'pesan', ]

		widgets = {
			'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Nama Anda', 'required': True}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Email', 'required': True}),
			'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan No. Hp', 'required': True}),
			'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukan Judul Pesan', 'required': True}),
			'pesan': forms.Textarea(attrs={'class': 'form-control', 'rows' : 5,'placeholder': 'Masukan Deskripsi Pesan', 'required': True}),
		}

		labels = {
			'nama': 'Nama',
			'email': 'Email',
			'no_hp': 'No. Hp (WA)',
			'judul': 'Judul',
			'pesan': 'Pesan'
		}


class BalasanPesanPelangganForm(forms.ModelForm):
	class Meta:
		model = BalasanPesanPelanggan
		fields = ['pesan_pelanggan', 'balasan']

		widgets = {
			'balasan': forms.Textarea(attrs={'class': 'form-control', 'rows' : 5, 'placeholder': 'Masukan Balasan Anda', 'required': True}),
		}

		labels = {
			'balasan': 'Balasan',
		}