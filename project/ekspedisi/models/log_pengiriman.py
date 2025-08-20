import os, datetime
from datetime import timedelta, datetime as dateAware
from random import randint
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

from .pengiriman import *
from .toko import *
from .gudang import *
from .user import *

def set_timezone() :
	return timezone.localtime(timezone.now())

class LogPengiriman(models.Model):

	id_pengiriman = models.ForeignKey(Pengiriman, related_name='log_pengiriman', on_delete=models.PROTECT)
	rute_pengiriman_outlet = models.ForeignKey(Toko, null=True, blank=True, on_delete=models.PROTECT)
	rute_pengiriman_gudang = models.ForeignKey(Gudang, null=True, blank=True, on_delete=models.PROTECT)
	rute_pengiriman_gudang_akhir = models.ForeignKey(Gudang, related_name='log_pengiriman_gudang_akhir', null=True, blank=True, on_delete=models.PROTECT)
	rute_pengiriman_outlet_akhir = models.ForeignKey(Toko, related_name='log_pengiriman_outlet_akhir', null=True, blank=True, on_delete=models.PROTECT)
	titik_lokasi = models.CharField(max_length=255, null=True, blank=True)
	id_kurir = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

	# API user 
	api_kurir_id = models.IntegerField(null=True, blank=True)
	api_kurir_name = models.CharField(max_length=100, null=True, blank=True)

	status_pengiriman= [
		('waiting', 'Waiting'),
		('pickup_by', 'Pickup By'),
		('sent_by', 'Sent By'),
		('arrive_at', 'Arrive At'),
		('done', 'Done')
	]

	status_pengiriman = models.CharField(max_length=50, choices=status_pengiriman)
	created_at = models.DateTimeField(default=set_timezone)
	updated_at = models.DateTimeField(default=set_timezone)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(str(self.id_pengiriman) + ' @ ' + str(self.created_at))