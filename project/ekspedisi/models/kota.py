import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .provinsi import *


class Kota(models.Model):
	nama_kota = models.CharField(max_length=255)
	provinsi_id = models.ForeignKey(Provinsi, related_name='kota_di_provinsi', null=True, blank=True, on_delete=models.SET_NULL)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.nama_kota)
