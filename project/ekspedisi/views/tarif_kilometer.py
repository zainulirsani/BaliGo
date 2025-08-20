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

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

def check_exist_tarif(data):
	try:
		if TarifKilometer.objects.filter(Q(is_active=True) & Q(jarak__iexact=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_exist_tarif_update(data, id):
	try:
		if TarifKilometer.objects.exclude(id=id).filter(Q(is_active=True) & Q(jarak__iexact=data)).exists():
			return False
		else:
			return True
	except:
		return True

@method_decorator(login_required, name='get')
class TarifKilometerView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = TarifKilometerForm()
		tarif_kilometer = list(TarifKilometer.objects.filter(is_active=True).values())
		data_list = []
		data_tarif_kilometer = []
		i = 1
		for data in tarif_kilometer:
			data_list = [i]
			data_list.append(data['id_tarif_kilometer'])
			data_list.append(str(data['jarak']) + ' Km')
			# data_list.append('Rp. ' + str(data['tarif']))
			data_list.append("Rp. {:,.2f}".format(data['tarif']))

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Tarif Kilometer" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editTarifKilometer"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Tarif" data-id="' + str(data['id']) + '" data-nama="' + str(data['jarak']) + '"class="btn btn-danger btn-sm deleteTarifKilometer"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div></center>')
			i =  i+1
			data_tarif_kilometer.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_tarif_kilometer}, status=200)

		return render(request, 'tarif_kilometer/index.html', context={'form': form, 'tarif_kilometer': data_tarif_kilometer})

	@csrf_exempt
	def post(self, request):
		try : 
			form = TarifKilometerForm(request.POST)
			if check_exist_tarif(data=request.POST.get("jarak")):
				if form.is_valid():
					try:
						new_tarif_kilometer = form.save(commit=False)
						new_tarif_kilometer.id_tarif_kilometer = generate_id('TK', 8)
						new_tarif_kilometer.save()
						return JsonResponse({'msg': 'Berhasil Menambah data Tarif Kilometer', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Kilometer {}'.format(e), 'type': 'error'}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Tarif Kilometer Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Tarif Untuk Jarak ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class TarifKilometerDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request, id):
		tarif_kilometer = TarifKilometer.objects.get(id=id)
		try:
			tarif_kilometer.is_active = False
			tarif_kilometer.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Tarif Kilometer (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Tarif Kilometer (Arsip)', 'type': 'error'}, status=443)


class TarifKilometerDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			tarif_kilometer = get_object_or_404(TarifKilometer, id = id)
			
			return JsonResponse({'data': model_to_dict(tarif_kilometer), 'msg': 'Berhasil Mengambil Data Tarif Kilometer', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Tarif Kilometer {}'.format(e), 'type': 'error'})

	def post(self, request, id):
		try: 
			obj = get_object_or_404(TarifKilometer, id = id)
			form = TarifKilometerForm(request.POST or None, instance = obj)
			if check_exist_tarif_update(data=request.POST.get("jarak"), id=id):
				if form.is_valid():
					try:
						form.save()
						
						return JsonResponse({'msg': 'Berhasil Update data Tarif Kilometer', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Menambah data Tarif Kilometer {}'.format(e), 'type': 'error'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data Tarif Kilometer Form Tidak Valid', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Tarif Untuk Jarak ini, Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

class HitungTarifKilometer(View):
	def get(self, request, kilometer):
		try:
			if kilometer == '0':
				return JsonResponse({'harga':''}, status=200)
			else:
				list_harga = list(TarifKilometer.objects.filter(is_active=True).values_list('jarak', flat=True))
				#Jika ada banyak list tarif kilometer, maka cari harga dengan kilometer terdekat dengan kilometer yg di input 
				
				jarak_terdekat = []
				id_tarif = []
				# for data in list_harga:
				# 	jarak = math.sqrt(math.pow((int(data['jarak'])-round(float(kilometer))), 2)) #eucledian distance
				# 	jarak_terdekat.append(jarak)
				# 	id_tarif.append(data['id'])

				#index_terdekat = jarak_terdekat.index(min(jarak_terdekat))
				#id_terdekat = id_tarif[index_terdekat] #id tarif kilometer yang digunakan untuk dikalikan dengan kilometer input

				try :
					jarak_terdekat_aktif = closest(list_harga, int(round(float(kilometer))))
					tarif_yang_digunakan = TarifKilometer.objects.filter(jarak=jarak_terdekat_aktif).latest('updated_at')
					if tarif_yang_digunakan :
						id_terdekat = tarif_yang_digunakan.id
						harga_mentah = float(tarif_yang_digunakan.tarif) * int(round(float(kilometer)))
						harga = round(harga_mentah / int(tarif_yang_digunakan.jarak))
					else :
						id_terdekat = 0
						tarif_yang_digunakan = 0
						harga = 0
				except Exception as e :
					print(e)
					raise Exception('Tidak menemukan tarif kilometer terdekat atau yang aktif')

				return JsonResponse({'harga': harga, 'jarak':jarak_terdekat_aktif, 'id_terdekat': id_terdekat, 'tarif_yang_digunakan':tarif_yang_digunakan.tarif}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})