from django import forms
from ..models import *

class POSForm(forms.ModelForm):
	class Meta:
		model = POS
		fields = ['id_pengiriman', 'nominal_bayar', 'total_tagihan', 'total_kembali']

		widgets = {
			'id_pengiriman': forms.HiddenInput(),
			'nominal_bayar': forms.HiddenInput(attrs={'class':'nominal_bayar_real'}),
			# 'nominal_bayar': forms.TextInput(attrs={'class': 'form-control nominal_bayar', 'placeholder': 'Masukkan Nominal yang dibayarkan pelanggan', 'id': 'inputBayarPengiriman', 'autofocus':'autofocus'}),
			'total_tagihan': forms.HiddenInput(),
			'total_kembali': forms.HiddenInput(attrs={'value':0}),
		}

		labels = {
            'nominal_bayar': 'Nominal Pembayaran',
            'total_tagihan': 'Total Tagihan',
            'total_kembali': 'Total Kembali',
            'id_pengiriman': 'Referensi Pengiriman'
        }