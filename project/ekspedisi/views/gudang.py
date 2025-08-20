from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime
import math
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
from .gudang_ambil_data import ambil_data_gudang

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

def deg2rad(deg):
	return deg * (math.pi/180)

def hitung_jarak(lat1, lon1, lat2, lon2):
	R = 6371 #radius of the earth in km
	dLat = deg2rad(lat2-lat1)
	dLon = deg2rad(lon2-lon1)
	a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = R * c #distance in KM
	return d

def check_(data):
	if not data :
		data = ''
	else :
		data.strip()
	try:
		if Gudang.objects.filter(nama_gudang__iexact=data).exists():
			return False
		else:
			return True
	except:
		return True

def check_data_update(data, id):
	try:
		if Gudang.objects.exclude(id=id).filter(Q(is_active=True) & Q(nama_gudang__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

class ListGudangView(View):
	def get(self, request, id):
		try:
			data = model_to_dict(get_object_or_404(Gudang, id = id))
			data_html = "<div class=\"timeline-item\"><span class=\"time\"><i class=\"fas fa-map-marker-alt\"></i> ("+str(data['titik_lokasi'])+")</span><p class=\"timeline-header no-border\"><small><span class=\"badge badge-warning\">Gudang #1</span> "+str(data['nama_gudang'])+" | Alamat: "+str(data['alamat'])+"</small></p></div>"
			if request.is_ajax():
				return JsonResponse({'data': data, 'data_html': data_html}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class ListGudangPenerimaView(View):
	def get(self, request, id):
		try:
			data = model_to_dict(get_object_or_404(Gudang, id = id))
			data_html = "<div class=\"timeline-item\"><span class=\"time\"><i class=\"fas fa-map-marker-alt\"></i> ("+str(data['titik_lokasi'])+")</span><p class=\"timeline-header no-border\"><small><span class=\"badge badge-warning\">Gudang #2</span> "+str(data['nama_gudang'])+" | Alamat: "+str(data['alamat'])+"</small></p></div>"
			if request.is_ajax():
				return JsonResponse({'data': data, 'data_html': data_html}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class GudangView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = GudangForm()
		gudangs = Gudang.objects.all()
		datas = list(Gudang.objects.values().all())
		data_list = []
		data_gudang = []
		i = 1
		for data in datas:
			data_list = [i]
			data_list.append(data['nama_gudang'])
			data_list.append(data['id_gudang'])
			data_list.append(data['alamat'])

			if data['is_active']:
				data_list.append('<span class="badge badge-success">Aktif</span><br>')
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Arsipkan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_gudang']) + '" class="btn btn-warning btn-sm arsipGudang"><i class="fa fa-fw fa-archive"></i></a>'
			else:
				data_list.append('<span class="badge badge-danger">Arsip</span><br>')
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Aktifkan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_gudang']) + '" class="btn btn-secondary btn-sm unarsipGudang"><i class="fa fa-fw fa-upload"></i></a>'

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Edit Gudang" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editGudang"><i class="fa fa-fw fa-edit"></i></a><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Gudang" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailGudang"><i class="fa fa-fw fa-eye"></i></a>'+btn_arsip+'<a href="javascript:void(0)" data-toggle="tooltip" title="Delete Gudang" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_gudang']) + '"class="btn btn-danger btn-sm deleteGudang"><i class="fa fa-fw fa-trash-alt"></i></a></div><center>')
			i =  i+1
			data_gudang.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_gudang}, status=200)

		return render(request, 'gudang/index.html', context={'form': form, 'gudangs': gudangs})

	@csrf_exempt
	def post(self, request):
		print
		form = GudangForm(request.POST)
		if check_(data = request.POST.get("nama_gudang")):
			if form.is_valid():
				try:
					new_gudang = form.save()
					return JsonResponse({'gudang': model_to_dict(new_gudang), 'msg': 'Berhasil Menambah data gudang', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Menambah data gudang: {}'.format(e), 'type': 'error'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Menambah Data, Form Input Tidak Valid', 'type': 'error'}, status=422)
		else:
			return JsonResponse({'msg': 'Nama Gudang Sudah Ada!', 'type': 'error'}, status=422)

class GudangDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			gudang = ambil_data_gudang(get_object_or_404(Gudang, id = request.GET.get('id')))
			return JsonResponse({'data': gudang, 'msg': 'Berhasil Mengambil Data Gudang', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Gudang: {}'.format(e), 'type': 'error'}, status=422)

	def post(self, request):
		try: 
			obj = get_object_or_404(Gudang, id = request.POST.get('id'))
			form = GudangForm(request.POST or None, instance = obj)
			if check_data_update(data = request.POST.get("nama_gudang"), id=request.POST.get('id')):
				if form.is_valid():
					form.save()
					return JsonResponse({'msg': 'Berhasil Update data Gudang', 'type': 'success'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data Gudang', 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Nama Gudang Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil data dari database : {}'.format(e), 'type': 'error'}, status=422)

class GudangDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		gudang = Gudang.objects.get(id=request.POST.get('id'))
		try:
			gudang.delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Gudang', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengapus Data Gudang, pastikan data transaksi tidak terkait di gudang ini'.format(e), 'type': 'error'}, status=443)

class GudangArsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		gudang = Gudang.objects.get(id=request.POST.get('id'))
		try:
			gudang.is_active = False
			gudang.save()
			return JsonResponse({'msg': 'Berhasil Mengarsipkan Data Gudang', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengarsipkan Data Gudang: {}'.format(e), 'type': 'error'}, status=443)

class GudangUnarsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		gudang = Gudang.objects.get(id=request.POST.get('id'))
		try:
			gudang.is_active = True
			gudang.save()
			return JsonResponse({'msg': 'Berhasil Mengaktifkan Data Gudang', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengaktifkan Data Gudang: {}'.format(e), 'type': 'error'}, status=443)

class GetAllGudang(View):
	def get(self, request):
		try:
			datas = list(Gudang.objects.values().filter(is_active = True))
			if request.is_ajax():
				return JsonResponse({'data': datas}, status=200)
			else:
				return JsonResponse({'data': datas}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Semua Gudang! : {}'.format(e), 'type': 'error'}, status=443)

class GetGudangByProvince(View):
	def post(self, request):
		try:
			id_provinsi = request.POST.get('province')
			data = ambil_data_gudang(Gudang.objects.filter(is_active = True, provinsi_gudang = id_provinsi).first())
			return JsonResponse({'data': data, 'msg': 'Sukses', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'data': '', 'msg': 'Gagal Mengambil data gudang: {}'.format(e), 'type': 'error'}, status=422)

class NearestGudang(View):
	def get(self, request, lat, lon):
		try:
			datas = list(Gudang.objects.values().filter(is_active = True))
			data_jarak = [];
			for data in datas:
				loc_gudang = data['titik_lokasi'].split(',') #lat, lon
				jarak = hitung_jarak(float(lat), float(lon), float(loc_gudang[0]), float(loc_gudang[1]))
				data_jarak.append(jarak);
			index_minimum = data_jarak.index(min(data_jarak))
			gudang_terpilih = datas[index_minimum]
			return JsonResponse({'data': gudang_terpilih}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)