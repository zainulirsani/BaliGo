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

class TentangView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = TentangForm()
		
		if request.is_ajax():
			try:
				tentang = list(Tentang.objects.values().filter(id = 1))
				data_list = []
				for data in tentang:
					data_list.append(data['id'])
					data_list.append(data['deskripsi'])
					data_list.append(data['created_at'])

				return JsonResponse({'data': data_list[1], 'msg': 'Berhasil Mengambil data Tentang', 'type': 'success'}, status=200)
			except:
				pass
				return JsonResponse({'data': '', 'msg': 'Gagal Mengambil data Tentang', 'type': 'error'})

		return render(request, 'tentang/index.html', context={'form': form})

	@csrf_exempt
	#UPDATE SECTION
	def post(self, request, id): 
		try: 
			obj = get_object_or_404(Tentang, id = id)
			form = TentangForm(request.POST or None, instance = obj)

			if form.is_valid():
				form.save()
				return JsonResponse({'msg': 'Berhasil Update data Tentang', 'type': 'success'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Update data Tentang', 'type': 'error'})
		except:
			form = TentangForm(request.POST)
			if form.is_valid():
				try:
					new_tentang = form.save()
					return JsonResponse({'data': model_to_dict(new_tentang), 'msg': 'Berhasil Menambah data Tentang', 'type': 'success'}, status=200)
				except:
					return JsonResponse({'msg': 'Gagal Menambah data Tentang', 'type': 'error'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Menambah Data, Form Input Tidak Valid', 'type': 'error'}, status=422)