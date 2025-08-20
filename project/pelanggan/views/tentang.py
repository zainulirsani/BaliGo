from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime
from random import randint

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from ekspedisi.models import *
from ekspedisi.forms import *

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission

from ekspedisi.views.custom_decorator import *


def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class PelangganTentangView(View):
	def get(self,request):
		try:
			tentang = Tentang.objects.get(id = 1)

			return render(request, 'frontend_pelanggan/templates/tentang/index.html', {'data':model_to_dict(tentang)})
		except:
			return render(request, 'frontend_pelanggan/templates/tentang/index.html', {'data':''})

class PelangganTentangAPI(View):
	def get(self, request):
		try:
			tentang = Tentang.objects.get(id=1)
			return JsonResponse({'data': model_to_dict(tentang), 'msg': 'Berhasil Mendapatkan Data Tentang', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'data': '', 'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=200)