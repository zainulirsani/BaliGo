import os, datetime
from datetime import timedelta
from random import randint
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel


class MapsApi(models.Model):
	api = models.CharField(max_length=200)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ['created_at']