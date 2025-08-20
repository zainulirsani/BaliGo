import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from .gudang import *

class TarifGudang(models.Model):
	id_tarif_gudang = models.CharField(max_length=200, blank=True, null=True)
	from_gudang = models.ForeignKey(Gudang, related_name='tarif_from_gudang', null=True, blank=True, on_delete=models.SET_NULL)
	to_gudang = models.ForeignKey(Gudang, related_name='tarif_to_gudang', null=True, blank=True, on_delete=models.SET_NULL)
	tarif = models.DecimalField(max_digits=16, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)