import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .user import *
from .pengemasan import *
from .toko import *
from .gudang import *
from .layanan import *
from .provinsi import *
from .kota import *
from .kecamatan import *
from .desa import *
from .kode_pos import *
from .satuan import *


def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()

class OrderPickup(models.Model):

	id_order = models.CharField(max_length=200, null=True, blank=True)
	id_customer = models.ForeignKey(User, related_name='pelanggan', on_delete=models.CASCADE, null=True, blank=True)
	jenis_barang = models.CharField(max_length=255)
	detail_barang = models.CharField(max_length=255)
	register_sebagai= [
		('personal', 'Personal'),
		('goverment', 'Goverment'),
		('company', 'Company'),
	]
	status_pengirim = models.CharField(max_length=20, choices=register_sebagai, default='personal', null=True, blank=True)

	jenis_pengiriman = models.ForeignKey(Layanan, related_name='orderpickup_layanan', on_delete=models.PROTECT)
	id_pengemasan = models.ForeignKey(Pengemasan, related_name='orderpickup_pengemasan', null=True, blank=True, on_delete=models.SET_NULL)

	provinsi_pengirim = models.ForeignKey(Provinsi, related_name='orderpickup_provinsi_pengirim', null=True, on_delete=models.PROTECT)
	kota_pengirim = models.ForeignKey(Kota, related_name='orderpickup_kota_pengirim', null=True, on_delete=models.PROTECT)
	kecamatan_pengirim = models.ForeignKey(Kecamatan, related_name='orderpickup_kecamatan_pengirim', null=True, on_delete=models.PROTECT)
	desa_pengirim = models.ForeignKey(Desa, related_name='orderpickup_desa_pengirim', null=True, on_delete=models.PROTECT)
	kode_pos_pengirim = models.ForeignKey(KodePos, related_name='orderpickup_kode_pos_pengirim', null=True, on_delete=models.PROTECT)
	alamat_pengirim_alt = models.TextField()

	nama_penerima = models.CharField(max_length=255)
	no_tlp_penerima = models.CharField(max_length=14)
	email_penerima = models.EmailField(max_length=254, blank=True)
	alamat_penerima = models.TextField()

	provinsi_penerima = models.ForeignKey(Provinsi, related_name='orderpickup_provinsi_penerima', null=True, on_delete=models.PROTECT)
	kota_penerima = models.ForeignKey(Kota, related_name='orderpickup_kota_penerima', null=True, on_delete=models.PROTECT)
	kecamatan_penerima = models.ForeignKey(Kecamatan, related_name='orderpickup_kecamatan_penerima', null=True, on_delete=models.PROTECT)
	desa_penerima = models.ForeignKey(Desa, related_name='orderpickup_desa_penerima', null=True, on_delete=models.PROTECT)
	kode_pos_penerima = models.ForeignKey(KodePos, related_name='orderpickup_kode_pos_penerima', null=True, on_delete=models.PROTECT)

	jumlah = models.IntegerField(default=1)
	satuan = models.ForeignKey(Satuan, related_name='satuan_order_pickup', null=True, on_delete=models.PROTECT)
	# Related ke biaya
	#tarif di kalkulasi di view untuk menghitung sub total, hasil nya akan otomatis muncul di input field tarif_berat, kilometer, gudang,layanan, dan total harga
	# berat = models.IntegerField(default=0)
	berat = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	tarif_berat = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	tarif_kilometer = models.DecimalField(max_digits=16, decimal_places=2, default=0, null=True, blank=True)
	tarif_gudang = models.DecimalField(max_digits=16, decimal_places=2, default=0, null=True, blank=True)
	tarif_layanan = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	total_tarif = models.IntegerField(default=0)
	extra_tarif_pengirim = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
	extra_tarif_penerima = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
	keterangan_extra_tarif = models.CharField(max_length=250, null=True, blank=True) #berisi keterangan extra tarif utk wilayah (desa, kec. kab. prov)

	id_toko = models.ForeignKey(Toko, related_name='toko', on_delete=models.PROTECT, null=True, blank=True,)
	id_gudang = models.ForeignKey(Gudang, related_name='gudang', on_delete=models.PROTECT, null=True, blank=True,)
	id_toko2 = models.ForeignKey(Toko, related_name='toko_penerimaan', on_delete=models.PROTECT, null=True, blank=True,)
	id_gudang2 = models.ForeignKey(Gudang, related_name='gudang_penerimaan', on_delete=models.PROTECT, null=True, blank=True,)

	status_order= [
		('waiting', 'Waiting'),
		('pickup', 'Pickup'),
		('cancel', 'Cancel Pickup'),
		('done', 'Done')
	]

	status = models.CharField(max_length=200, choices=status_order, default="waiting")
	source = models.CharField(max_length=100, blank=True, null=True, default='internal_apps')
	keterangan_cancel = models.CharField(max_length=200, null=True, blank=True)
	scan_by = models.ForeignKey(User, related_name="orderpickup_scan", on_delete=models.SET_NULL, null=True, blank=True, default=None)
	kurir_id = models.ForeignKey(User, related_name="orderpickup_dispatch", on_delete=models.SET_NULL, null=True, blank=True, default=None)


	#Untuk user API (Isi ID dan Nama jika menggunakan database luar)
	api_nama_pengirim = models.CharField(max_length=255, null=True, blank=True)
	api_no_tlp_pengirim = models.CharField(max_length=14, null=True, blank=True)
	api_email_pengirim = models.EmailField(max_length=254, blank=True, null=True, default='ekspedisi@api.com')
	api_alamat_pengirim = models.TextField(null=True, blank=True)
	api_scan_by_id = models.IntegerField(null=True, blank=True)
	api_scan_by_user_name = models.CharField(max_length=200, blank=True, null=True)
	api_source_name_apps = models.CharField(max_length=100, blank=True, null=True)
	api_order_id_apps = models.IntegerField(null=True, blank=True)

	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at']

	def __str__(self) :
		try :
			return str(self.id_order)
		except :
			pass