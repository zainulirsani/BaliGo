from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime
from random import randint

from django.http import JsonResponse, HttpResponse
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

class ProvinsiView(View):
	def post(self, request):
		try:
			datas = list(Provinsi.objects.values().filter(is_active = True))
			data_provinsi = ""
			for data in datas:
				data_provinsi += '<option value="'+str(data['id'])+'">'+str(data['nama_provinsi'])+'</option>'
			if request.is_ajax():
				return JsonResponse({'data': data_provinsi}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class KotaView(View):
	def post(self, request, provinsi_id):
		try:
			datas = list(Kota.objects.values().filter(provinsi_id = provinsi_id))
			data_kota = ""
			for data in datas:
				data_kota += '<option value="'+str(data['id'])+'">'+str(data['nama_kota'])+'</option>'
			if request.is_ajax():
				return JsonResponse({'data': data_kota}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class KecamatanView(View):
	def post(self, request, kota_id):
		try:
			datas = list(Kecamatan.objects.values().filter(kota_id = kota_id))
			data_kecamatan = ""
			for data in datas:
				data_kecamatan += '<option value="'+str(data['id'])+'">'+str(data['nama_kecamatan'])+'</option>'
			if request.is_ajax():
				return JsonResponse({'data': data_kecamatan}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class DesaView(View):
	def post(self, request, kecamatan_id):
		try:
			datas = list(Desa.objects.values().filter(kecamatan_id = kecamatan_id))
			data_desa = ""
			for data in datas:
				data_desa += '<option value="'+str(data['id'])+'">'+str(data['nama_desa'])+'</option>'
			if request.is_ajax():
				return JsonResponse({'data': data_desa}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class KodePosView(View):
	def post(self, request, provinsi_id, kota_id, kecamatan_id, desa_id):
		try:
			datas = list(KodePos.objects.values().filter(provinsi_id = provinsi_id, kota_id = kota_id, kecamatan_id = kecamatan_id, desa_id = desa_id))
			data_kode = ""
			for data in datas:
				data_kode += '<option value="'+str(data['id'])+'">'+str(data['kode_pos'])+'</option>'
			if request.is_ajax():
				return JsonResponse({'data': data_kode}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)