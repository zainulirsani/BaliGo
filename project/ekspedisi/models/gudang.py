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

class Gudang(models.Model):
	id_gudang = models.CharField(max_length=16, unique=True)
	nama_gudang = models.CharField(max_length=255)
	radius = models.IntegerField(default=500)
	no_tlp = models.CharField(max_length=14)
	alamat = models.TextField()
	titik_lokasi = models.CharField(max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	provinsi_gudang = models.ForeignKey(Provinsi, related_name='provinsi_gudang', null=True, on_delete=models.PROTECT)
	kota_gudang = models.ForeignKey(Kota, related_name='kota_gudang', null=True, on_delete=models.PROTECT)
	kecamatan_gudang = models.ForeignKey(Kecamatan, related_name='kecamatan_gudang', null=True, on_delete=models.PROTECT)
	desa_gudang = models.ForeignKey(Desa, related_name='desa_gudang', null=True, on_delete=models.PROTECT)
	kode_pos_gudang = models.ForeignKey(KodePos, related_name='kode_pos_gudang', null=True, on_delete=models.PROTECT)

	def __str__(self) :
		return str(self.nama_gudang) or self.id_gudang

	class Meta:
		ordering = ['created_at']