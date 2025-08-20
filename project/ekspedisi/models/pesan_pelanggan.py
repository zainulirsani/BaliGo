import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()

class PesanPelanggan(models.Model):
	nama = models.CharField(max_length=150)
	email = models.EmailField(max_length=100)
	no_hp = models.CharField(max_length=16)
	judul = models.CharField(max_length=150)
	pesan = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.judul) or "Tidak Ditentukan"

class BalasanPesanPelanggan(models.Model):
	pesan_pelanggan = models.ForeignKey(PesanPelanggan, related_name='balasan_pesan_pelanggan', on_delete=models.CASCADE)
	balasan = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	def __str__(self) :
		return str(self.balasan) or "Tidak Ditentukan"