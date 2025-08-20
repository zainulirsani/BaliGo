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

def check_exist_tarif(data):
	try:
		if TarifLayanan.objects.filter(Q(is_active=True) & Q(layanan_id=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_exist_tarif_update(data, id):
	try:
		if TarifLayanan.objects.exclude(id=id).filter(Q(is_active=True) & Q(layanan_id=data)).exists():
			return False
		else:
			return True
	except:
		return True

@method_decorator(login_required, name='get')
class TarifLayananView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = TarifLayananForm()
		tarif_layanan = list(TarifLayanan.objects.filter(is_active=True).values())
		data_list = []
		data_tarif_layanan = []
		i = 1
		for data in tarif_layanan:
			data_list = [i]
			layanan = model_to_dict(get_object_or_404(Layanan, id = data['layanan_id']))
			data_list.append(data['id_tarif_layanan'])
			data_list.append(layanan['nama_layanan'])
			# data_list.append('Rp. ' + str(data['tarif']))
			data_list.append("Rp. {:,.2f}".format(data['tarif']))

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Tarif Layanan" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editTarifLayanan"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Tarif" data-id="' + str(data['id']) + '" data-nama="' + str(layanan['nama_layanan']) + '"class="btn btn-danger btn-sm deleteTarifLayanan"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div></center>')
			i =  i+1
			data_tarif_layanan.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_tarif_layanan}, status=200)

		return render(request, 'tarif_layanan/index.html', context={'form': form, 'tarif_layanan': data_tarif_layanan})

	@csrf_exempt
	def post(self, request):
		try :  
			form = TarifLayananForm(request.POST)
			if check_exist_tarif(data=request.POST.get("layanan")):
				if form.is_valid():
					try:
						new_tarif_layanan = form.save(commit=False)
						new_tarif_layanan.id_tarif_layanan = generate_id('TL', 8)
						new_tarif_layanan.save()
						return JsonResponse({'msg': 'Berhasil Menambah data Tarif Layanan', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Layanan {}'.format(e), 'type': 'error'}, status=422)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Tarif Layanan Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Tarif Untuk Layanan ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=422)


class TarifLayananDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		tarif_layanan = TarifLayanan.objects.get(id=request.POST.get('id'))
		try:
			tarif_layanan.is_active = False
			tarif_layanan.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Tarif Layanan (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Tarif Layanan (Arsip)', 'type': 'error'}, status=422)


class TarifLayananDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			tarif_layanan = get_object_or_404(TarifLayanan, id = request.GET.get('id'))
			if tarif_layanan.layanan:
				data_layanan = model_to_dict(get_object_or_404(Layanan, id=tarif_layanan.layanan.id))
			else:
				data_layanan = '' 
			return JsonResponse({'data': model_to_dict(tarif_layanan), 'layanan': data_layanan, 'msg': 'Berhasil Mengambil Data Tarif Layanan', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Tarif Layanan {}'.format(e), 'type': 'error'}, status=422)

	def post(self, request):
		try: 
			obj = get_object_or_404(TarifLayanan, id = request.POST.get('id'))
			form = TarifLayananForm(request.POST or None, instance = obj)

			if check_exist_tarif_update(data=request.POST.get("layanan"), id = request.POST.get('id')):
				if form.is_valid():
					try:
						form.save()
						
						return JsonResponse({'msg': 'Berhasil Update data Tarif Layanan', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Layanan {}'.format(e), 'type': 'error'}, status=422)
				else:
					return JsonResponse({'msg': 'Gagal Update data Tarif Layanan Form Tidak Valid', 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Tarif Untuk Layanan ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=422)

class HitungTarifLayanan(View):
	def get(self, request, id_layanan):
		try:
			print(id_layanan)
			if id_layanan == '0':
				return JsonResponse({'harga':''}, status=200)
			else:
				harga_layanan = TarifLayanan.objects.filter(layanan_id=id_layanan, is_active=True).latest('updated_at')
				if harga_layanan :
					tarif = harga_layanan.tarif
				else :
					tarif = 0
				return JsonResponse({'harga':tarif}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error', 'harga': '0'})

class SemuaTarifLayanan(View):
	def get(self, request):
		try:
			# tarif_layanan = list(TarifLayanan.objects.filter(is_active=True).prefetch_related('tarif_layanan_nama').values())
			# print(tarif_layanan)
			data_list = []

			# for data in tarif_layanan:
			# 	layanan = model_to_dict(get_object_or_404(Layanan, id = data['layanan_id']))
			# 	print(layanan)
			# 	if layanan['publish_status'] == True and layanan['is_active'] == True:
			# 		data_list.append({'id_tarif_layanan': data['id_tarif_layanan'], 'nama_layanan': layanan['nama_layanan'], 'harga': data['tarif'], 'estimasi': layanan['estimasi_layanan']})

			layanan = list(Layanan.objects.filter(is_active=True, publish_status=True).values())
			for data in layanan :
				try :
					tarif_layanan = model_to_dict(TarifLayanan.objects.filter(layanan_id = data['id']).latest('updated_at'))
					if tarif_layanan['is_active'] == True :
						data_list.append({'id_tarif_layanan': tarif_layanan['id_tarif_layanan'], 'nama_layanan': data['nama_layanan'], 'harga': tarif_layanan['tarif'], 'estimasi': data['estimasi_layanan']})
				except :
					data_list.append({'id_tarif_layanan': "", 'nama_layanan': data['nama_layanan'], 'harga': '', 'estimasi': ""})
					pass

			return JsonResponse({'data': data_list}, status=200)
		except Exception as e:
			print(e)
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type':'error'})