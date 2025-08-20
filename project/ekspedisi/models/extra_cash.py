import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .gudang import *

class ExtraCash(models.Model):
	data_wilayah = [
		('desa', 'Desa'),
		('kecamatan', 'Kecamatan'),
		('kabupaten', 'Kabupaten/Kota'),
		('provinsi', 'provinsi')
	]
	wilayah = models.CharField(max_length=50, choices=data_wilayah)
	tarif = models.DecimalField(max_digits=16, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)