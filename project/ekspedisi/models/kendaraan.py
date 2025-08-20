import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .toko import *
from .gudang import *

def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()


class Kendaraan(models.Model):

	id_kendaraan = models.CharField(max_length=200, blank=True, null=True)
	nama_kendaraan = models.CharField(max_length=25)
	no_kendaraan = models.CharField(max_length=12, unique=True)
	type_choices = [
		('mobil', 'Mobil'),
		('motor', 'Motor'),
		('truck', 'Truck')
	]
	type_bahan_bakar = [
		('bensin', 'Bensin'),
		('solar', 'Solar'),
	]
	jenis_kendaraan = models.CharField(max_length=50, choices=type_choices)
	penempatan_toko	  = models.ForeignKey(Toko, related_name="kendaraan_toko", null=True, blank=True, on_delete=models.SET_NULL)
	penempatan_gudang = models.ForeignKey(Gudang, related_name="kendaraan_gudang", null=True, blank=True, on_delete=models.SET_NULL)
	kapasitas_tank = models.CharField(max_length=6)
	bahan_bakar = models.CharField(max_length=50, choices=type_bahan_bakar)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.nama_kendaraan + ' NO PLAT: ' + str(self.no_kendaraan))



