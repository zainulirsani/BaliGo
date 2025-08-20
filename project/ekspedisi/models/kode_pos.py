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

class KodePos(models.Model):
	desa_id = models.ForeignKey(Desa, related_name='kodepos_di_desa', null=True, blank=True, on_delete=models.SET_NULL)
	kecamatan_id = models.ForeignKey(Kecamatan, related_name='kodepos_di_kecamatan', null=True, blank=True, on_delete=models.SET_NULL)
	kota_id = models.ForeignKey(Kota, related_name='kodepos_di_kota', null=True, blank=True, on_delete=models.SET_NULL)
	provinsi_id = models.ForeignKey(Provinsi, related_name='kodepos_di_provinsi', null=True, blank=True, on_delete=models.SET_NULL)
	kode_pos = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.kode_pos)