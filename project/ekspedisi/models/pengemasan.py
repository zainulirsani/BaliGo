import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()

class Pengemasan(models.Model):

	id_pengemasan = models.CharField(max_length=200, null=True, blank=True)
	nama_pengemasan = models.CharField(max_length=200)
	bahan_pengemasan = models.CharField(max_length=200)
	tarif = models.DecimalField(max_digits=16, decimal_places=2, default=0)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		try :
			return str(self.nama_pengemasan + ' - ' + self.tarif)
		except :
			return str(self.nama_pengemasan+ '-' + str(self.tarif))