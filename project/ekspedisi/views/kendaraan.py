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
		if Kendaraan.objects.filter(Q(no_kendaraan__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_data_update(data, id):
	try:
		if Kendaraan.objects.exclude(id=id).filter(Q(no_kendaraan__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

class KendaraanView(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = KendaraanForm()

		if request.user.is_authenticated:
			is_admin = request.user.is_superuser
		else:
			is_admin = False

		if is_admin:
			kendaraan = list(Kendaraan.objects.all().values())
		else:
			try:
				outlet_tugas = request.user.penempatan_toko.id
				is_outlet = True
			except:
				outlet_tugas = 0
				is_outlet = False
			try:
				gudang_tugas = request.user.penempatan_gudang.id
				is_gudang = True
			except:
				gudang_tugas = 0
				is_gudang = False

			if is_outlet:
				kendaraan = list(Kendaraan.objects.filter(Q(penempatan_toko_id=outlet_tugas)).values())
			elif is_gudang:
				kendaraan = list(Kendaraan.objects.filter(Q(penempatan_gudang_id=gudang_tugas)).values())

		data_list = []
		data_kendaraan = []
		i = 1
		for data in kendaraan:
			data_list = [i]
			data_list.append(data['id_kendaraan'])
			data_list.append(data['nama_kendaraan'])
			data_list.append(data['no_kendaraan'])
			data_list.append(data['jenis_kendaraan'])

			if data['penempatan_toko_id']:
				data_toko = model_to_dict(get_object_or_404(Toko, id = data['penempatan_toko_id']))
				data_list.append('Outlet: ' + data_toko['nama_toko'])
			elif data['penempatan_gudang_id']:
				data_gudang = model_to_dict(get_object_or_404(Gudang, id = data['penempatan_gudang_id']))
				data_list.append('Gudang: ' + data_gudang['nama_gudang'])
			else:
				data_list.append('Kosong')

			data_list.append(data['kapasitas_tank'])
			data_list.append(data['bahan_bakar'])

			if is_admin:
				btn_delete = '<a href="javascript:void(0)" data-toggle="tooltip" title="Delete Kendaraan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_kendaraan']) + '"class="btn btn-danger btn-sm deleteKendaraan"><i class="fa fa-fw fa-trash-alt"></i></a>'
			else:
				btn_delete = ''

			if data['is_active'] == True:
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Arsipkan Kendaraan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_kendaraan']) + '"class="btn btn-warning btn-sm arsipKendaraan"><i class="fa fa-fw fa-archive"></i></a>'
			else:
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Kembalikan Kendaraan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_kendaraan']) + '"class="btn btn-success btn-sm unarsipKendaraan"><i class="fa fa-fw fa-upload"></i></a>'

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Edit Kendaraan" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editKendaraan"><i class="fa fa-fw fa-edit"></i></a>' + btn_arsip + btn_delete + '</div></center>')
			i =  i+1
			data_kendaraan.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_kendaraan}, status=200)

		return render(request, 'kendaraan/index.html', context={'form': form, 'kendaraan': data_kendaraan})

	@csrf_exempt
	def post(self, request):
		try : 
			form = KendaraanForm(request.POST)
			if check_(data = request.POST.get("no_kendaraan")):
				if form.is_valid():
					try:
						new_kendaraan = form.save(commit=False)
						new_kendaraan.id_kendaraan = generate_id('KN', 8)
						new_kendaraan.save()
						return JsonResponse({'msg': 'Berhasil Menambah data Kendaraan', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Kendaraan {}'.format(e), 'type': 'error'}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Kendaraan Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Nomor Kendaraan Sudah Ada!', 'type': 'error'}, status=422)

		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class KendaraanDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			kendaraan = Kendaraan.objects.get(id=request.POST.get('id'))
			kendaraan.delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Kendaraan', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Kendaraan', 'type': 'error'}, status=422)

class KendaraanArsip(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			kendaraan = Kendaraan.objects.get(id=request.POST.get('id'))
			kendaraan.is_active = False
			kendaraan.save()
			return JsonResponse({'msg': 'Berhasil Mengarsip Data Kendaraan', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Kendaraan', 'type': 'error'}, status=422)

class KendaraanUnarsip(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			kendaraan = Kendaraan.objects.get(id=request.POST.get('id'))
			kendaraan.is_active = True
			kendaraan.save()
			return JsonResponse({'msg': 'Berhasil Mengembalikan Data Kendaraan', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengembalikan Data Kendaraan', 'type': 'error'}, status=422)


class KendaraanDetail(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			kendaraan = get_object_or_404(Kendaraan, id = request.GET.get('id'))

			if kendaraan.penempatan_gudang:
				data_gudang = kendaraan.penempatan_gudang.nama_gudang
				id_gudang = kendaraan.penempatan_gudang.id
			else:
				data_gudang = ''
				id_gudang = ''

			if kendaraan.penempatan_toko:
				data_toko = kendaraan.penempatan_toko.nama_toko
				id_toko = kendaraan.penempatan_toko.id
			else:
				data_toko = ''
				id_toko = ''
			
			data = {
				'id': kendaraan.id,
				'id_kendaraan': kendaraan.id_kendaraan,
				'nama_kendaraan': kendaraan.nama_kendaraan,
				'no_kendaraan': kendaraan.no_kendaraan,
				'jenis_kendaraan': kendaraan.jenis_kendaraan,
				'kapasitas_tank': kendaraan.kapasitas_tank,
				'bahan_bakar': kendaraan.bahan_bakar,
				'nama_gudang': data_gudang,
				'id_gudang': id_gudang,
				'nama_toko': data_toko,
				'id_toko': id_toko
			}
			
			return JsonResponse({'data': data, 'msg': 'Berhasil Mengambil Data Kendaraan', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Kendaraan {}'.format(e), 'type': 'error'})

	def post(self, request):
		try: 
			obj = get_object_or_404(Kendaraan, id = request.POST.get('id'))
			form = KendaraanForm(request.POST or None, instance = obj)
			if check_data_update(data = request.POST.get("no_kendaraan"), id=request.POST.get('id')):
				if form.is_valid():
					try:
						form.save()
						
						return JsonResponse({'msg': 'Berhasil Update data Kendaraan', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Menambah data Kendaraan {}'.format(e), 'type': 'error'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data Kendaraan Form Tidak Valid', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Nomor Kendaraan Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})