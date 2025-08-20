import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .toko import *
from .gudang import *
from .provinsi import *
from .kota import *
from .kecamatan import *
from .desa import *
from .kode_pos import *

def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()


class User(AbstractUser, TimeStampedModel) :
	no_personil = models.CharField(max_length=200, null=True, blank=True)
	no_telp 	= models.CharField(max_length=15)
	alamat	 	= models.CharField(max_length=200, default=None, null=True, blank=True)
	photo 		= models.ImageField(upload_to='users_photo/%Y/%m/%d/', null=True, blank=True)
	email		= models.EmailField(max_length=50, unique=True, error_messages={'unique':"Email sudah digunakan"})

	role_choices= [
	('adm_gudang', 'Admin Gudang'),
	('adm_outlet', 'Admin Outlet'),
	('kurir', 'Kurir')
	]

	role			  = models.CharField(max_length=50, choices=role_choices, null=True, blank=True)
	penempatan_toko	  = models.ForeignKey(Toko, related_name="personil_toko", null=True, blank=True, on_delete=models.SET_NULL)
	penempatan_gudang = models.ForeignKey(Gudang, related_name="personil_gudang", null=True, blank=True, on_delete=models.SET_NULL)
	
	register_sebagai= [
		('personal', 'Personal'),
		('goverment', 'Goverment'),
		('company', 'Company'),
	]
	register_sebagai = models.CharField(max_length=20, choices=register_sebagai, null=True, blank=True)
	is_active = models.BooleanField(default=True)
	is_api_user = models.BooleanField(default=False)


	def __str__(self) :
		return str(self.username)

	class Meta:
		verbose_name = "User"

class InformasiPelanggan(models.Model) :
	pelanggan_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='pelanggan_detail',
        primary_key=True,
    )
	provinsi = models.ForeignKey(Provinsi, related_name='provinsi_pelanggan', null=True, on_delete=models.SET_NULL)
	kota = models.ForeignKey(Kota, related_name='kota_pelanggan', null=True, on_delete=models.SET_NULL)
	kecamatan = models.ForeignKey(Kecamatan, related_name='kecamatan_pelanggan', null=True, on_delete=models.SET_NULL)
	desa = models.ForeignKey(Desa, related_name='desa_pelanggan', null=True, on_delete=models.SET_NULL)
	kode_pos = models.ForeignKey(KodePos, related_name='kode_pos_pelanggan', null=True, on_delete=models.SET_NULL)