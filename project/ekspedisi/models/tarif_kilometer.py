import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

class TarifKilometer(models.Model):
	id_tarif_kilometer = models.CharField(max_length=200, blank=True, null=True)
	jarak = models.IntegerField()
	tarif = models.DecimalField(max_digits=16, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_active = models.BooleanField(default=True)