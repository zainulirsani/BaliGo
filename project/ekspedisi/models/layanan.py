import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()

class Layanan(models.Model):
	nama_layanan = models.CharField(max_length=100)
	estimasi_layanan = models.FloatField()
	deskripsi = models.CharField(max_length=200)
	publish_status = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.nama_layanan) or "Tidak Ditentukan"