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
		if TarifBerat.objects.filter(Q(is_active=True) & Q(berat__iexact=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_exist_tarif_update(data, id):
	try:
		if TarifBerat.objects.exclude(id=id).filter(Q(is_active=True) & Q(berat__iexact=data)).exists():
			return False
		else:
			return True
	except:
		return True

@method_decorator(login_required, name='get')
class TarifBeratView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = TarifBeratForm()
		tarif_berat = list(TarifBerat.objects.filter(is_active=True).values())
		data_list = []
		data_tarif_berat = []
		i = 1
		for data in tarif_berat:
			data_list = [i]
			data_list.append(data['id_tarif_berat'])
			data_list.append(str(data['berat']) + ' Kg')
			# data_list.append('Rp. ' + str(data['tarif']))
			data_list.append("Rp. {:,.2f}".format(data['tarif']))
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Tarif Berat" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editTarifBerat"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Tarif" data-id="' + str(data['id']) + '" data-nama="' + str(data['berat']) + '"class="btn btn-danger btn-sm deleteTarifBerat"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div></center>')
			i =  i+1
			data_tarif_berat.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_tarif_berat}, status=200)

		return render(request, 'tarif_berat/index.html', context={'form': form, 'tarif_berat': data_tarif_berat})

	@csrf_exempt
	def post(self, request):
		try : 
			form = TarifBeratForm(request.POST)
			if check_exist_tarif(data=request.POST.get("berat")):
				if form.is_valid():
					try:
						new_tarif_berat = form.save(commit=False)
						new_tarif_berat.id_tarif_berat = generate_id('TK', 8)
						new_tarif_berat.save()
						return JsonResponse({'msg': 'Berhasil Menambah data Tarif Berat', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Berat {}'.format(e), 'type': 'error'}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Tarif Berat Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Tarif Untuk berat ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class TarifBeratDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request, id):
		tarif_berat = TarifBerat.objects.get(id=id)
		try:
			tarif_berat.is_active = False
			tarif_berat.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Tarif Berat (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Tarif Berat (Arsip)', 'type': 'error'}, status=443)


class TarifBeratDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			tarif_berat = get_object_or_404(TarifBerat, id = id)
			
			return JsonResponse({'data': model_to_dict(tarif_berat), 'msg': 'Berhasil Mengambil Data Tarif Berat', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Tarif Berat {}'.format(e), 'type': 'error'})

	def post(self, request, id):
		try: 
			obj = get_object_or_404(TarifBerat, id = id)
			form = TarifBeratForm(request.POST or None, instance = obj)
			if check_exist_tarif_update(data=request.POST.get("berat"),id=id):
				if form.is_valid():
					try:
						form.save()
						
						return JsonResponse({'msg': 'Berhasil Update data Tarif Berat', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Berat {}'.format(e), 'type': 'error'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data Tarif Berat Form Tidak Valid', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Tarif Untuk berat ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})


class HitungTarifBerat(View):
	def get(self, request, berat):
		try:
			if berat == '0':
				return JsonResponse({'harga':''}, status=200)
			else:
				list_harga = list(TarifBerat.objects.filter(is_active=True).values())
				#Jika ada banyak list Tarif Berat, maka cari harga dengan berat terdekat dengan berat yg di input 
				
				jarak_terdekat = []
				id_tarif = []
				for data in list_harga:
					jarak = math.sqrt(math.pow((float(data['berat'])-float(berat)), 2)) #eucledian distance
					jarak_terdekat.append(jarak)
					id_tarif.append(data['id'])

				index_terdekat = jarak_terdekat.index(min(jarak_terdekat))
				id_terdekat = id_tarif[index_terdekat] #id Tarif Berat yang digunakan untuk dikalikan dengan berat input

				try :
					tarif_yang_digunakan = model_to_dict(TarifBerat.objects.filter(berat=int(berat), is_active=1).latest('created_at'))
					harga = float(float(int(tarif_yang_digunakan['tarif']) / float(tarif_yang_digunakan['berat'])) * int(berat))
				except Exception as e:
					print(e)
					tarif_yang_digunakan = model_to_dict(get_object_or_404(TarifBerat, id = id_terdekat))
					# harga = float(tarif_yang_digunakan['tarif']) * float(berat)
					harga = float(float(int(tarif_yang_digunakan['tarif']) / float(tarif_yang_digunakan['berat'])) * int(berat))
				harga = round(harga)
				print(harga)
				
				return JsonResponse({'harga': harga, 'jarak':jarak_terdekat, 'id_terdekat': id_terdekat, 'tarif_yang_digunakan':tarif_yang_digunakan['tarif']}, status=200)
		except Exception as e:
			return JsonResponse({'harga': 0, 'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})