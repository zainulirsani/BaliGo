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
		print(data)
		if Pengemasan.objects.filter(Q(is_active=True) & Q(nama_pengemasan__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_data_update(data, id):
	try:
		if Pengemasan.objects.exclude(id=id).filter(Q(is_active=True) & Q(nama_pengemasan__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True


class PengemasanView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = PengemasanForm()
		pengemasan = list(Pengemasan.objects.filter(is_active=True).values())
		data_list = []
		data_pengemasan = []
		i = 1
		for data in pengemasan:
			data_list = [i]
			data_list.append(data['id_pengemasan'])
			data_list.append(data['nama_pengemasan'])
			data_list.append(data['bahan_pengemasan'])
			# data_list.append('Rp. '+str(data['tarif']))
			data_list.append("Rp. {:,.2f}".format(data['tarif']))

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Pengemasan" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editPengemasan"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Pengemasan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_pengemasan']) + '"class="btn btn-danger btn-sm deletePengemasan"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div></center>')
			i =  i+1
			data_pengemasan.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_pengemasan}, status=200)

		return render(request, 'pengemasan/index.html', context={'form': form, 'pengemasan': data_pengemasan})

	@csrf_exempt
	def post(self, request):
		try : 
			form = PengemasanForm(request.POST)
			if check_(data = request.POST.get("nama_pengemasan")):
				if form.is_valid():
					try:
						new_pengemasan = form.save(commit=False)
						new_pengemasan.id_pengemasan = generate_id('PK', 8)
						new_pengemasan.save()
						return JsonResponse({'msg': 'Berhasil Menambah data Pengemasan', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Pengemasan {}'.format(e), 'type': 'error'}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Pengemasan Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Nama Pengemasan Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class PengemasanDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		pengemasan = Pengemasan.objects.get(id=request.POST.get('id'))
		try:
			pengemasan.is_active = False
			pengemasan.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Pengemasan (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Pengemasan (Arsip)', 'type': 'error'}, status=443)


class PengemasanDetail(View):
	# @method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			pengemasan = get_object_or_404(Pengemasan, id = request.GET.get('id'))
			
			return JsonResponse({'data': model_to_dict(pengemasan), 'msg': 'Berhasil Mengambil Data Pengemasan', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Pengemasan {}'.format(e), 'type': 'error'})

	def post(self, request):
		try: 
			obj = get_object_or_404(Pengemasan, id = request.POST.get('id'))
			form = PengemasanForm(request.POST or None, instance = obj)
			if check_data_update(data = request.POST.get("nama_pengemasan"), id=request.POST.get('id')):
				if form.is_valid():
					try:
						form.save()
						
						return JsonResponse({'msg': 'Berhasil Update data Pengemasan', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Menambah data Pengemasan {}'.format(e), 'type': 'error'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data Pengemasan Form Tidak Valid', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Nama Pengemasan Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})