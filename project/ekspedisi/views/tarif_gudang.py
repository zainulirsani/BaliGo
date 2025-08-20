from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.db.models import Q

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

def check_exist_tarif(data1, data2):
	try:
		if TarifGudang.objects.filter(Q(is_active=True) & Q((Q(from_gudang_id=data1) & Q(to_gudang_id=data2)) | (Q(from_gudang_id=data2) & Q(to_gudang_id=data1)))).exists():
			return False
		else:
			return True
	except:
		return True

def check_exist_tarif_update(data1, data2, id):
	try:
		if TarifGudang.objects.exclude(id=id).filter(Q(is_active=True) & Q((Q(from_gudang_id=data1) & Q(to_gudang_id=data2)) | (Q(from_gudang_id=data2) & Q(to_gudang_id=data1)))).exists():
			return False
		else:
			return True
	except:
		return True

@method_decorator(login_required, name='get')
class TarifGudangView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = TarifGudangForm()
		tarif_gudang = list(TarifGudang.objects.filter(is_active=True).values())
		data_list = []
		data_tarif_gudang = []
		i = 1
		for data in tarif_gudang:
			data_list = [i]
			
			data_list.append(data['id_tarif_gudang'])
			try:
				from_gudang = model_to_dict(get_object_or_404(Gudang, id = data['from_gudang_id']))
				data_list.append(from_gudang['nama_gudang'])
			except:
				data_list.append('Kosong')

			try:
				to_gudang = model_to_dict(get_object_or_404(Gudang, id = data['to_gudang_id']))
				data_list.append(to_gudang['nama_gudang'])
			except:
				data_list.append('Kosong')
			# data_list.append('Rp. ' + str(data['tarif']))
			data_list.append("Rp. {:,.2f}".format(data['tarif']))

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Tarif Gudang" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editTarifGudang"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Tarif" data-id="' + str(data['id']) + '" data-nama="' + str(from_gudang['nama_gudang']) + '"class="btn btn-danger btn-sm deleteTarifGudang"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div></center>')
			i =  i+1
			data_tarif_gudang.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_tarif_gudang}, status=200)

		return render(request, 'tarif_gudang/index.html', context={'form': form, 'tarif_gudang': data_tarif_gudang})

	@csrf_exempt
	def post(self, request):
		try : 
			form = TarifGudangForm(request.POST)
			if check_exist_tarif(request.POST.get('from_gudang'), request.POST.get('to_gudang')):
				if form.is_valid():
					try:
						new_tarif_gudang = form.save(commit=False)
						new_tarif_gudang.id_tarif_gudang = generate_id('TG', 8)
						new_tarif_gudang.save()
						return JsonResponse({'msg': 'Berhasil Menambah data Tarif Gudang', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Gudang {}'.format(e), 'type': 'error'}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Tarif Gudang Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Tarif Untuk Antar Gudang ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class TarifGudangDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request, id):
		tarif_gudang = TarifGudang.objects.get(id=id)
		try:
			tarif_gudang.is_active = False
			tarif_gudang.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Tarif Gudang (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Tarif Gudang (Arsip)', 'type': 'error'}, status=443)


class TarifGudangDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			try :
				tarif_gudang = get_object_or_404(TarifGudang, id = id)
			except :
				tarif_gudang = list(TarifGudang.objects.none().values())

			try :
				from_gudang = get_object_or_404(Gudang, id=tarif_gudang.from_gudang_id)
			except :
				from_gudang = list(Gudang.objects.none().values())

			try :
				to_gudang = get_object_or_404(Gudang, id=tarif_gudang.to_gudang_id)
			except :
				to_gudang = list(Gudang.objects.none().values())

			if tarif_gudang :
				tarif_gudang = model_to_dict(tarif_gudang)
			if from_gudang :
				from_gudang = model_to_dict(from_gudang)
			if to_gudang :
				to_gudang = model_to_dict(to_gudang)

			return JsonResponse({'data': tarif_gudang, 'from_gudang':from_gudang, 'to_gudang':to_gudang, 'msg': 'Berhasil Mengambil Data Tarif Gudang', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Tarif Gudang {}'.format(e), 'type': 'error'})

	def post(self, request, id):
		try: 
			if check_exist_tarif_update(request.POST.get('from_gudang'), request.POST.get('to_gudang'), id):
				obj = get_object_or_404(TarifGudang, id = id)
				form = TarifGudangForm(request.POST or None, instance = obj)

				if form.is_valid():
					try:
						form.save()
						
						return JsonResponse({'msg': 'Berhasil Update data Tarif Gudang', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Gudang {}'.format(e), 'type': 'error'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data Tarif Gudang Form Tidak Valid', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Tarif Untuk Antar Gudang ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})


class HitungTarifGudang(View):
	def get(self, request, id_gudang_1, id_gudang_2):
		try:
			tarif = list(TarifGudang.objects.filter(Q(is_active=True) & (Q(from_gudang_id=id_gudang_1, to_gudang_id=id_gudang_2) | Q(from_gudang_id=id_gudang_2, to_gudang_id=id_gudang_1))).values())

			if tarif:
				return JsonResponse({'data': tarif[0], 'msg': 'Berhasil Mendapatkan tarif gudang', 'type': 'success'}, status=200)
			else:

				return JsonResponse({'data': '0', 'msg': 'Data Master Tarif gudang Seperti belum terdaftar untuk gudang tersebut', 'type': 'error'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})