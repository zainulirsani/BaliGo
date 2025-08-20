import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .kota import *


class Kecamatan(models.Model):
	nama_kecamatan = models.CharField(max_length=255)
	kota_id = models.ForeignKey(Kota, related_name='kecamatan_di_kota', null=True, blank=True, on_delete=models.SET_NULL)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.nama_kecamatan)
