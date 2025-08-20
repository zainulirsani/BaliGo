from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import math
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
		if ExtraCash.objects.filter(Q(is_active=True) & Q(wilayah__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

@method_decorator(login_required, name='get')
class ExtraCashView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = ExtraCashForm()
		ec = list(ExtraCash.objects.filter(is_active=True).values())
		data_list = []
		data_tarif_ec = []
		i = 1
		for data in ec:
			data_list = [i]
			data_list.append(data['wilayah'])
			data_list.append("Rp. {:,.2f}".format(data['tarif']))
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Tarif Extra Cash" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editExtraCash"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Extra Cash" data-id="' + str(data['id']) + '" data-nama="' + str(data['wilayah']) + '"class="btn btn-danger btn-sm deleteExtraCash"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div></center>')
			i =  i+1
			data_tarif_ec.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_tarif_ec}, status=200)

		return render(request, 'extra_cash/index.html', context={'form': form, 'data': data_tarif_ec})

	@csrf_exempt
	def post(self, request):
		try : 
			check_asrip = ExtraCash.objects.filter(is_active=False, wilayah=request.POST.get("wilayah")).count()
			
			if check_asrip > 0:
				data_arsip = ExtraCash.objects.get(Q(is_active=False) & Q(wilayah=request.POST.get("wilayah")))
				return JsonResponse({'msg': 'Username/Email Sudah ada pada data arsip', 'type': 'warning', 'data_arsip': model_to_dict(data_arsip), 'arsip': True}, status=200)
			
			else:
				form = ExtraCashForm(request.POST)
				if check_exist_tarif(data=request.POST.get("wilayah")):
					if form.is_valid():
						try:
							new_ec = form.save()
							return JsonResponse({'msg': 'Berhasil Menambah data Extra Cash', 'type': 'success', 'arsip': False}, status=200)
						except Exception as e :
							return JsonResponse({'msg': 'Gagal Menambah data Extra Cash {}'.format(e), 'type': 'error', 'arsip': False}, status=400)
					else:
						error = [er[0] for er in form.errors.values()]
						error = "<br> ".join(error)
						return JsonResponse({'msg': 'Gagal, Form Tarif Extra Cash Tidak Valid <br> {}'.format(error), 'type': 'error', 'arsip': False}, status=422)
				else:
					return JsonResponse({'msg': 'Tarif Untuk Extra Cash ini, Sudah Ada!', 'type': 'error', 'arsip': False}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error', 'arsip': False}, status=400)


class ExtraCashDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		id_ec = request.POST.get('id')
		EC = ExtraCash.objects.get(id=id_ec)
		try:
			EC.is_active = False
			EC.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Tarif Extra Cash (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Tarif Extra Cash (Arsip)', 'type': 'error'}, status=443)


class ExtraCashDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			id_ec = request.POST.get('id')
			EC = get_object_or_404(ExtraCash, id = id_ec)
			
			return JsonResponse({'data': model_to_dict(EC), 'msg': 'Berhasil Mengambil Data Tarif Extra Cash', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Tarif Extra Cash {}'.format(e), 'type': 'error'})

class ExtraCashUpdate(View):
	def post(self, request):
		try:
			id_ec = request.POST.get('id')
			obj = get_object_or_404(ExtraCash, id = id_ec)
			form = ExtraCashForm(request.POST or None, instance = obj)

			if form.is_valid():
				try:
					form.save()
					return JsonResponse({'msg': 'Berhasil Update data Tarif Extra Cash', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Menambah data Tarif Extra Cash {}'.format(e), 'type': 'error'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Update data Tarif Extra Cash Form Tidak Valid', 'type': 'error'})
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})

class ExtraCashActivate(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			EC = ExtraCash.objects.get(id=request.POST.get("id"))
			EC.is_active = True
			EC.save()
			return JsonResponse({'msg': 'Berhasil Merestore Extra Cash', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=422)

class GetExtraCash(View):
	def get(self, request):
		try:
			wilayah = request.GET.get('wilayah')
			ec = ExtraCash.objects.get(wilayah=wilayah, is_active=True)
			harga = ec.tarif
			daerah = ec.wilayah
			return JsonResponse({'harga': harga, 'wilayah': daerah}, status=200)
		except:
			return JsonResponse({'harga': '0', 'wilayah': ''}, status=200)