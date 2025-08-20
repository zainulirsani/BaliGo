import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

from .provinsi import *
from .kota import *
from .kecamatan import *
from .desa import *
from .kode_pos import *

def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()

class Toko(models.Model):
	nama_toko = models.CharField(max_length=255)
	radius = models.IntegerField(default=500)
	id_toko = models.CharField(max_length=16, unique=True)
	alamat = models.TextField()
	kontak = models.CharField(max_length=14, blank=True, null=True)
	titik_lokasi = models.CharField(max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	is_active = models.BooleanField(default=True)

	provinsi_toko = models.ForeignKey(Provinsi, related_name='provinsi_toko', null=True, on_delete=models.PROTECT)
	kota_toko = models.ForeignKey(Kota, related_name='kota_toko', null=True, on_delete=models.PROTECT)
	kecamatan_toko = models.ForeignKey(Kecamatan, related_name='kecamatan_toko', null=True, on_delete=models.PROTECT)
	desa_toko = models.ForeignKey(Desa, related_name='desa_toko', null=True, on_delete=models.PROTECT)
	kode_pos_toko = models.ForeignKey(KodePos, related_name='kode_pos_toko', null=True, on_delete=models.PROTECT)


	def __str__(self) :
		return str(self.nama_toko) or self.id_toko

	class Meta:
		ordering = ['created_at'] 