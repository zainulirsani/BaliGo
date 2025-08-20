import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

def user_img(instance, filename) :
    return 'user_{0}/{1}'.format(instance.username, filename).strip()

class Tentang(models.Model):
	deskripsi = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ['created_at']