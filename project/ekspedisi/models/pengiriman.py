import os, datetime
from datetime import timedelta, datetime as dateAware
from random import randint
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

from .provinsi import *
from .kota import *
from .kecamatan import *
from .desa import *
from .kode_pos import *
from .layanan import *
from .pengemasan import *
from .tarif_kilometer import *
from .tarif_gudang import *
from .user import *
from .toko import *
from .satuan import *
from .order_pickup import *
import random
import string

def set_timezone() :
	return timezone.localtime(timezone.now())

class Pengiriman(models.Model):
	id_pengiriman = models.CharField(max_length=200, null=True, blank=True) #resi
	outlet_pengiriman = models.ForeignKey(Toko, related_name='toko_pengiriman', null=True, on_delete=models.PROTECT) #outlet/ toko tempat barang di terima
	gudang_pengiriman = models.ForeignKey(Gudang, related_name='gudang_pengiriman', null=True, on_delete=models.PROTECT) #outlet/ toko tempat barang di terima
	nama_pengirim = models.CharField(max_length=200)
	#data apakah pengirim sebagai personal, goverment, company (order pickup)
	register_sebagai= [
		('personal', 'Personal'),
		('goverment', 'Goverment'),
		('company', 'Company'),
	]
	status_pengirim = models.CharField(max_length=20, choices=register_sebagai, default='personal', null=True, blank=True)
	no_telp_pengirim = models.CharField(max_length=200)
	email_pengirim = models.EmailField(max_length=200, default='ekspedisi@samitra.com')
	alamat_pengirim = models.CharField(max_length=200)

	provinsi_pengirim = models.ForeignKey(Provinsi, related_name='provinsi_pengiriman', null=True, on_delete=models.PROTECT)
	kota_pengirim = models.ForeignKey(Kota, related_name='kota_pengiriman', null=True, on_delete=models.PROTECT)
	kecamatan_pengirim = models.ForeignKey(Kecamatan, related_name='kecamatan_pengiriman', null=True, on_delete=models.PROTECT)
	desa_pengirim = models.ForeignKey(Desa, related_name='desa_pengiriman', null=True, on_delete=models.PROTECT)
	kode_pos_pengirim = models.ForeignKey(KodePos, related_name='kode_pos_pengiriman', null=True, on_delete=models.PROTECT)

	nama_penerima = models.CharField(max_length=200)
	no_telp_penerima = models.CharField(max_length=200)
	email_penerima = models.EmailField(max_length=200, default='ekspedisi@samitra.com')
	alamat_penerima = models.CharField(max_length=200)

	provinsi_penerima = models.ForeignKey(Provinsi, related_name='provinsi_penerima', null=True, on_delete=models.PROTECT)
	kota_penerima = models.ForeignKey(Kota, related_name='kota_penerima', null=True, on_delete=models.PROTECT)
	kecamatan_penerima = models.ForeignKey(Kecamatan, related_name='kecamatan_penerima', null=True, on_delete=models.PROTECT)
	desa_penerima = models.ForeignKey(Desa, related_name='desa_penerima', null=True, on_delete=models.PROTECT)
	kode_pos_penerima = models.ForeignKey(KodePos, related_name='kode_pos_penerima', null=True, on_delete=models.PROTECT)

	outlet_penerimaan = models.ForeignKey(Toko, related_name='toko_penerima', null=True, on_delete=models.PROTECT) #otomatis select toko/outlet terdekat dengan alamat penerima
	gudang_penerimaan = models.ForeignKey(Gudang, related_name='gudang_penerima', null=True, on_delete=models.PROTECT) #otomatis select toko/outlet terdekat dengan alamat penerima
	jenis_barang = models.CharField(max_length=100)
	detail_barang = models.CharField(max_length=255, null=True, blank=True)
	pengemasan = models.ForeignKey(Pengemasan, related_name='pengemasan_pengiriman', null=True, on_delete=models.PROTECT)
	layanan = models.ForeignKey(Layanan, related_name='layanan_pengiriman', on_delete=models.PROTECT)
	# berat = models.IntegerField()
	berat = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	jumlah = models.IntegerField(default=1)
	satuan = models.ForeignKey(Satuan, related_name='satuan_pengiriman', null=True, on_delete=models.PROTECT)

	# Pencatat Pengiriman (Admin Outlet)
	pencatat = models.ForeignKey(User, related_name='pencatat', on_delete=models.PROTECT, null=True, blank=True)

	# Pencatat API user (jika tidak menggunakan database User Django)
	api_pencatat_by_id = models.IntegerField(null=True, blank=True)
	api_pencatat_by_user_name = models.CharField(max_length=200, blank=True, null=True)
	api_source_name_apps = models.CharField(max_length=100, blank=True, null=True)
	api_pengiriman_id_apps = models.IntegerField(null=True, blank=True)

	#tarif di kalkulasi di view untuk menghitung sub total, hasil nya akan otomatis muncul di input field tarif_berat, kilometer, gudang,layanan, dan total harga
	tarif_berat = models.DecimalField(max_digits=16, decimal_places=2)
	tarif_pengemasan = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, default=0)
	tarif_lain = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, default=0)
	tarif_kilometer = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, default=0)
	tarif_gudang = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, default=0)
	tarif_layanan = models.DecimalField(max_digits=16, decimal_places=2)
	extra_tarif_pengirim = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, default=0)
	extra_tarif_penerima = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, default=0)
	keterangan_extra_tarif = models.CharField(max_length=250, null=True, blank=True) #berisi keterangan extra tarif utk wilayah (desa, kec. kab. prov)
	total_tarif = models.IntegerField()

	source = models.CharField(max_length=100, blank=True, null=True, default='admin')
	order_pickup = models.ForeignKey(OrderPickup, related_name='orderpickup_pengiriman', null=True, blank=True, on_delete=models.SET_NULL)
	created_at = models.DateTimeField(default=set_timezone)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.id_pengiriman)

class POS(models.Model) :
	no_transaksi = models.CharField(max_length=200, null=True, blank=True) #resi
	id_pengiriman = models.ForeignKey(Pengiriman, related_name='pengiriman', null=True, on_delete=models.CASCADE) #aku ganti jadi Cascade karena di pengiriman ada fitur delete khusus untuk admin,
	nominal_bayar = models.DecimalField(max_digits=16, decimal_places=2)
	total_tagihan = models.DecimalField(max_digits=16, decimal_places=2)
	total_kembali = models.DecimalField(max_digits=16, decimal_places=2)
	created_at = models.DateTimeField(default=set_timezone)
	is_active = models.BooleanField(default=True)

class TandaTerima(models.Model) :
	id_pengiriman = models.ForeignKey(Pengiriman, related_name='tanda_terima', null=True, on_delete=models.CASCADE)
	nama_penerima = models.CharField(max_length=30, null=True, default='Ybs')
	keterangan = models.CharField(max_length=50, null=True, blank=True)
	created_at = models.DateTimeField(default=set_timezone)

class BuktiFotoTandaTerima(models.Model) :
	id_ttd = models.ForeignKey(TandaTerima, related_name='bukti_foto', null=True, on_delete=models.CASCADE)
	foto = models.ImageField(upload_to='bukti_ttd/%Y/%m/%d/{rts}{rand}/'.format(rts=''.join(random.choice(string.ascii_lowercase) for i in range(10)), rand=randint(1,9)), null=True, blank=True)