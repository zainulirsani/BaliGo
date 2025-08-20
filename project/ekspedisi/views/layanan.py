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
from django.db.models import Q
from .custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

def check_(data):
	try:
		if Layanan.objects.filter(Q(is_active=True) & Q(nama_layanan__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_data_update(data, id):
	try:
		if Layanan.objects.exclude(id=id).filter(Q(is_active=True) & Q(nama_layanan__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_tarif_layanan(id_layanan, status_publish, status_active):
	try:
		# print(status_publish)
		if status_publish == 'on' and status_active == True:
			data_tarif = TarifLayanan.objects.get(is_active=False, layanan_id=id_layanan)
			data_tarif.is_active = True
			data_tarif.save()
			return True
		elif status_publish == None and status_active == True:
			data_tarif = TarifLayanan.objects.get(is_active=True, layanan_id=id_layanan)
			data_tarif.is_active = False
			data_tarif.save()
			return False
		elif status_publish == None and status_active == False:
			data_tarif = TarifLayanan.objects.get(is_active=True, layanan_id=id_layanan)
			data_tarif.is_active = False
			data_tarif.save()
			return False
		else:
			data_tarif = TarifLayanan.objects.get(is_active=True, layanan_id=id_layanan)
			data_tarif.is_active = False
			data_tarif.save()
			return False
	except:
		return False

class LayananView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = LayananForm()
		layanan = Layanan.objects.all()
		datas = list(Layanan.objects.values().filter(is_active = True))
		data_list = []
		data_layanan = []
		i = 1
		for data in datas:
			data_list = [i]
			data_list.append(data['nama_layanan'])
			data_list.append(data['estimasi_layanan'])
			data_list.append(data['deskripsi'])
			status_layanan = "Aktif" if data['publish_status'] else "Tidak Aktif" 
			data_list.append(status_layanan)
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Layanan" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editLayanan"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Layanan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_layanan']) + '"class="btn btn-danger btn-sm deleteLayanan"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div><center>')
			i =  i+1
			data_layanan.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_layanan}, status=200)

		return render(request, 'layanan/index.html', context={'form': form, 'layanan': layanan})

	@csrf_exempt
	def post(self, request):
		form = LayananForm(request.POST)
		if check_(data = request.POST.get("nama_layanan")):
			if form.is_valid():
				try:
					new_layanan = form.save()
					return JsonResponse({'layanan': model_to_dict(new_layanan), 'msg': 'Berhasil Menambah data layanan', 'type': 'success'}, status=200)
				except:
					return JsonResponse({'msg': 'Gagal Menambah data layanan', 'type': 'error'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Menambah Data, Form Input Tidak Valid', 'type': 'error'}, status=422)
		else:
			return JsonResponse({'msg': 'Nama Layanan Sudah Ada!', 'type': 'error'}, status=422)

class LayananDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			layanan = get_object_or_404(Layanan, id = request.GET.get('id'))
			return JsonResponse({'data': model_to_dict(layanan), 'msg': 'Berhasil Mengambil Data Layanan', 'type': 'success'})
		except:
			return JsonResponse({'msg': 'Gagal Mengambil Data Layanan', 'type': 'error'})

	def post(self, request):
		try: 
			obj = get_object_or_404(Layanan, id = request.POST.get('id'))
			form = LayananForm(request.POST or None, instance = obj)
			if check_data_update(data = request.POST.get("nama_layanan"), id=request.POST.get('id')):
				check_tarif_layanan(obj.id, request.POST.get("publish_status"), obj.is_active)
				if form.is_valid():
					form.save()
					return JsonResponse({'msg': 'Berhasil Update data Layanan', 'type': 'success'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data layanan', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Nama Layanan Sudah Ada!', 'type': 'error'}, status=422)
		except:
			return JsonResponse({'msg': 'Gagal Mengambil data dari database!', 'type': 'error'})

class LayananDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		layanan = Layanan.objects.get(id=request.POST.get('id'))
		try:
			layanan.is_active = False
			layanan.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Layanan (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Layanan (Arsip)', 'type': 'error'}, status=443)