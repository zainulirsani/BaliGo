from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime, math
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
from .toko_ambil_data import ambil_data_toko

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
	try:
		if Toko.objects.filter(Q(is_active=True) & Q(nama_toko__icontains=data)).exists():
			return False
		else:
			return True
	except Exception as e:
		return False

def check_data_update(data, id):
	try:
		if Toko.objects.exclude(id=id).filter(nama_toko__icontains=data).exists():
			return False
		else:
			return True
	except:
		return True

class TokoView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self,request):
		form = TokoForm()
		tokos = Toko.objects.all()
		tokonya = list(Toko.objects.values().all())
		data_list = []
		data_toko = []
		i = 1
		for toko in tokonya:
			data_list = [i]
			data_list.append(toko['nama_toko'])
			data_list.append(toko['id_toko'])
			data_list.append(toko['alamat'])
			if toko['is_active']:
				data_list.append('<span class="badge badge-success">Aktif</span><br>')
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Arsipkan" data-id="' + str(toko['id']) + '" data-nama="' + str(toko['nama_toko']) + '" class="btn btn-warning btn-sm arsipToko"><i class="fa fa-fw fa-archive"></i></a>'
			else:
				data_list.append('<span class="badge badge-danger">Arsip</span><br>')
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Aktifkan" data-id="' + str(toko['id']) + '" data-nama="' + str(toko['nama_toko']) + '" class="btn btn-secondary btn-sm unarsipToko"><i class="fa fa-fw fa-upload"></i></a>'

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Edit Outlet" data-id="' + str(toko['id']) + '" class="edit btn btn-primary btn-sm editToko"><i class="fa fa-fw fa-edit"></i></a><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Outlet" data-id="' + str(toko['id']) + '" class="btn btn-success btn-sm detailToko"><i class="fa fa-fw fa-eye"></i></a>'+btn_arsip+'<a href="javascript:void(0)" title="Hapus Outlet" data-toggle="modal" data-id="' + str(toko['id']) + '" data-nama="'+ toko['nama_toko'] +'" class="btn btn-danger btn-sm modalcolor deleteToko" data-modalcolor="#ff6666"><i class="fas fa-trash-alt"></i></a></div></center>')
			i =  i+1
			data_toko.extend([data_list])
		
		if request.is_ajax():
			return JsonResponse({'data': data_toko}, status=200)
		return render(request, 'toko/index.html', context={'form': form, 'tokos': tokos})

	def post(self, request):
		form = TokoForm(request.POST)
		if check_(data = request.POST.get("nama_toko")):
			if form.is_valid():
				try:
					new_toko = form.save()
					return JsonResponse({'toko': model_to_dict(new_toko), 'msg': 'Berhasil Menambah data Outlet', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Menambah data Outlet {}'.format(e), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Gagal Menambah Data, Form Input Tidak Valid / Id Outlet sudah terdaftar', 'type': 'error'}, status=422)
		else:
			return JsonResponse({'msg': 'Nama Outlet Sudah Ada!', 'type': 'error'}, status=422)


class TokoDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		toko = Toko.objects.get(id=request.POST.get('id'))
		try:
			toko.delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Outlet', 'type': 'success'}, status=200)
		except Exception as e:
			print(e)
			return JsonResponse({'msg': 'Gagal Mengapus Data Outlet, pastikan data transaksi tidak terkait di outlet ini', 'type': 'error'}, status=443)

class TokoArsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		toko = Toko.objects.get(id=request.POST.get('id'))
		try:
			toko.is_active = False
			toko.save()
			return JsonResponse({'msg': 'Berhasil Mengarsip Data Outlet', 'type': 'success'}, status=200)
		except Exception as e:
			print(e)
			return JsonResponse({'msg': 'Gagal Mengarsip Data Outlet, silahkan mencoba kembali beberapa saat kemudian', 'type': 'error'}, status=443)

class TokoUnarsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		toko = Toko.objects.get(id=request.POST.get('id'))
		try:
			toko.is_active = True
			toko.save()
			return JsonResponse({'msg': 'Berhasil Mengaktifkan Data Outlet', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengaktifkan Data Outlet: {}'.format(e), 'type': 'error'}, status=443)


class TokoUpdate(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			toko = ambil_data_toko(get_object_or_404(Toko, id = request.GET.get('id')))
			print(toko)
			return JsonResponse({'data': toko, 'msg': 'Berhasil Mengambil Data Outlet', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Outlet {}'.format(e), 'type': 'error'}, status=422)

	def post(self, request):
		try: 
			obj = get_object_or_404(Toko, id = request.POST.get('id'))
			form = TokoForm(request.POST or None, instance = obj)
			if check_data_update(data = request.POST.get("nama_toko"), id=request.POST.get('id')):
				if form.is_valid():
					form.save()
					return JsonResponse({'msg': 'Berhasil Update data Outlet', 'type': 'success'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data Outlet (Harap Isi Setiap Field)', 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Nama Outlet Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil data dari database!: {}'.format(e), 'type': 'error'}, status=422)

class ListOutletView(View):
	def post(self, request, id):
		try:
			data = model_to_dict(get_object_or_404(Toko, id = id))
			data_html = "<div class=\"timeline-item\"><span class=\"time\"><i class=\"fas fa-map-marker-alt\"></i> ("+str(data['titik_lokasi'])+")</span><p class=\"timeline-header no-border\"><small><span class=\"badge badge-warning\">Outlet #1</span> "+str(data['nama_toko'])+" | Alamat: "+str(data['alamat'])+"</small></p></div>"
			if request.is_ajax():
				return JsonResponse({'data': data, 'data_html': data_html}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class ListOutletPenerimaView(View):
	def get(self, request, id):
		try:
			data = model_to_dict(get_object_or_404(Toko, id = id))
			data_html = "<div class=\"timeline-item\"><span class=\"time\"><i class=\"fas fa-map-marker-alt\"></i> ("+str(data['titik_lokasi'])+")</span><p class=\"timeline-header no-border\"><small><span class=\"badge badge-warning\">Outlet #2</span> "+str(data['nama_toko'])+" | Alamat: "+str(data['alamat'])+"</small></p></div>"
			if request.is_ajax():
				return JsonResponse({'data': data, 'data_html': data_html}, status=200)
			else:
				return HttpResponse('Ops.. your request is not process')
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class calculate_last_outlet(View):
	def get(self, request, lat, lon):
		try:
			datas = list(Toko.objects.values().filter(is_active = True))
			data_jarak = [];
			for data in datas:
				loc_toko = data['titik_lokasi'].split(',') #lat, lon
				jarak = hitung_jarak(float(lat), float(lon), float(loc_toko[0]), float(loc_toko[1]))
				data_jarak.append(jarak);
			index_minimum = data_jarak.index(min(data_jarak))
			outlet_terpilih = datas[index_minimum]
			data_html = "<div class=\"timeline-item\"><span class=\"time\"><i class=\"fas fa-map-marker-alt\"></i> ("+str(outlet_terpilih['titik_lokasi'])+")</span><p class=\"timeline-header no-border\"><small><span class=\"badge badge-warning\">Outlet #2</span> "+str(outlet_terpilih['nama_toko'])+" | Alamat: "+str(outlet_terpilih['alamat'])+"</small></p></div>"
			if request.is_ajax():
				return JsonResponse({'data': outlet_terpilih, 'data_html': data_html}, status=200)
			return JsonResponse({'data': outlet_terpilih}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class NearestOutlet(View):
	def get(self, request, lat, lon):
		try:
			datas = list(Toko.objects.values().filter(is_active = True))
			data_jarak = [];
			for data in datas:
				loc_toko = data['titik_lokasi'].split(',') #lat, lon
				jarak = hitung_jarak(float(lat), float(lon), float(loc_toko[0]), float(loc_toko[1]))
				data_jarak.append(jarak);
			index_minimum = data_jarak.index(min(data_jarak))
			outlet_terpilih = datas[index_minimum]
			data_html = "<div class=\"timeline-item\"><span class=\"time\"><i class=\"fas fa-map-marker-alt\"></i> ("+str(outlet_terpilih['titik_lokasi'])+")</span><p class=\"timeline-header no-border\"><small><span class=\"badge badge-warning\">Outlet #1</span> "+str(outlet_terpilih['nama_toko'])+" | Alamat: "+str(outlet_terpilih['alamat'])+"</small></p></div>"
			if request.is_ajax():
				return JsonResponse({'data': outlet_terpilih, 'data_html': data_html}, status=200)
			return JsonResponse({'data': outlet_terpilih}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)