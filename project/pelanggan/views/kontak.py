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

class PelangganKontakView(View):
	# @method_decorator(user_customer_check(path_url='/customer/login/'))
	def get(self,request):
		try:
			form = PesanPelangganForm()
			kontak = Kontak.objects.get(id = 1)
			
			return render(request, 'frontend_pelanggan/templates/kontak/index.html', {'data':model_to_dict(kontak), 'form': form})
		except:
			return render(request, 'frontend_pelanggan/templates/kontak/index.html', {'data':'', 'form': form})

	def post(self, request):
		form = PesanPelangganForm(request.POST)
		if form.is_valid():
			try:
				new_pesan = form.save()
				return JsonResponse({'pesan': model_to_dict(new_pesan), 'msg': 'Berhasil mengirim pesan', 'type': 'success'}, status=200)
			except:
				return JsonResponse({'msg': 'Gagal mengirim pesan', 'type': 'error'}, status=200)
		else:
			return JsonResponse({'msg': 'Gagal mengirim pesan, Form Input Tidak Valid', 'type': 'error'}, status=422)