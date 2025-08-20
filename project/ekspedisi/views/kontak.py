from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime
from random import randint

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import *
from ..forms import *

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission

from .custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class KontakView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = KontakForm()
		if request.is_ajax():
			try:
				kontak = list(Kontak.objects.values().filter(id = 1))
				data_list = []
				for data in kontak:
					data_list.append(data['alamat'])
					data_list.append(data['no_tlp'])
					data_list.append(data['email'])

				return JsonResponse({'alamat': data_list[0],'no_tlp': data_list[1],'email': data_list[2], 'msg': 'Berhasil Mengambil data Kontak', 'type': 'success'}, status=200)
			except:
				pass
				return JsonResponse({'data': '', 'msg': 'Gagal Mengambil data Kontak', 'type': 'error'})

		return render(request, 'kontak/index.html', context={'form': form})

	@csrf_exempt
	#UPDATE SECTION
	def post(self, request, id): 
		try: 
			obj = get_object_or_404(Kontak, id = id)
			form = KontakForm(request.POST or None, instance = obj)

			if form.is_valid():
				form.save()
				return JsonResponse({'msg': 'Berhasil Update data Kontak', 'type': 'success'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Update data Kontak', 'type': 'error'})
		except:
			form = KontakForm(request.POST)
			if form.is_valid():
				try:
					new_kontak = form.save()
					return JsonResponse({'data': model_to_dict(new_kontak), 'msg': 'Berhasil Menambah data Kontak', 'type': 'success'}, status=200)
				except:
					return JsonResponse({'msg': 'Gagal Menambah data Kontak', 'type': 'error'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Menambah Data, Form Input Tidak Valid', 'type': 'error'}, status=422)