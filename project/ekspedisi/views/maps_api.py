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

class MapsApiView(View):
	def get(self, request):
		form = MapsApiForm()
		MapsApi = MapsApi.objects.all()
		datas = list(MapsApi.objects.values().filter(is_active = True))
		data_list = []
		data_MapsApi = []
		i = 1
		for data in datas:
			data_list = [i]
			data_list.append(data['api'])
			data_list.append(data['created_at'])
			status_MapsApi = "Aktif" if data['is_active'] else "Tidak Aktif" 
			data_list.append(status_MapsApi)
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit MapsApi" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editMapsApi"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete MapsApi" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_MapsApi']) + '"class="btn btn-danger btn-sm deleteMapsApi"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div><center>')
			i =  i+1
			data_MapsApi.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_MapsApi}, status=200)

		return render(request, 'MapsApi/index.html', context={'form': form, 'MapsApi': MapsApi})

	@csrf_exempt
	def post(self, request):
		form = MapsApiForm(request.POST)
		if form.is_valid():
			try:
				new_MapsApi = form.save()
				return JsonResponse({'MapsApi': model_to_dict(new_MapsApi), 'msg': 'Berhasil Menambah data MapsApi', 'type': 'success'}, status=200)
			except:
				return JsonResponse({'msg': 'Gagal Menambah data MapsApi', 'type': 'error'}, status=200)
		else:
			return JsonResponse({'msg': 'Gagal Menambah Data, Form Input Tidak Valid', 'type': 'error'}, status=422)

class MapsDetail(View):
	def get(self, request, id):
		try:
			MapsApi = get_object_or_404(MapsApi, id = id)
			return JsonResponse({'data': model_to_dict(MapsApi), 'msg': 'Berhasil Mengambil Data MapsApi', 'type': 'success'})
		except:
			return JsonResponse({'msg': 'Gagal Mengambil Data MapsApi', 'type': 'error'})

	def post(self, request, id):
		try: 
			obj = get_object_or_404(MapsApi, id = id)
			form = MapsApiForm(request.POST or None, instance = obj)

			if form.is_valid():
				form.save()
				return JsonResponse({'msg': 'Berhasil Update data MapsApi', 'type': 'success'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Update data MapsApi', 'type': 'error'})
		except:
			return JsonResponse({'msg': 'Gagal Mengambil data dari database!', 'type': 'error'})

class MapsDelete(View):
	def post(self, request, id):
		Maps = MapsApi.objects.get(id=id)
		try:
			Maps.is_active = False
			Maps.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data MapsApi (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data MapsApi (Arsip)', 'type': 'error'}, status=443)

class GetApiKey(View):
	def get(self, request):
		try:
			apikey = MapsApi.objects.filter(is_active=True)[0]
			return JsonResponse({'data': model_to_dict(apikey)})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Api Key {}'.format(e), 'type': 'error'})