import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .kecamatan import *


class Desa(models.Model):
	nama_desa = models.CharField(max_length=255)
	kecamatan_id = models.ForeignKey(Kecamatan, related_name='desa_di_kecamatan', null=True, blank=True, on_delete=models.SET_NULL)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.nama_desa)