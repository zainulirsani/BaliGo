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

@method_decorator(login_required, name='get')
class PersonilView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self,request):
		form = PersonilForm()
		personil = list(User.objects.exclude(is_staff=True).exclude(role="kurir").exclude(register_sebagai="personal").exclude(register_sebagai="company").exclude(register_sebagai="goverment").filter(is_active=True).values())
		data_list = []
		data_personil = []
		i = 1
		switcher = {
			"adm_gudang" : "Admin Gudang",
			"adm_outlet" : "Admin Outlet",
			"kurir" : "Kurir"
		}
		for data in personil:
			data_list = [i]
			data_list.append(data['no_personil'])
			data_list.append(data['first_name'])
			data_list.append(data['email'])
			data_list.append(data['no_telp'])
			role = switcher.get(data['role'], "-")
			data_list.append(role)
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Personil" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editPersonil"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Detail Personil" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailPersonil"><i class="fa fa-fw fa-eye"></i> Detail</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Delete Personil" data-id="' + str(data['id']) + '" data-nama="' + str(data['first_name']) + '"class="btn btn-danger btn-sm deletePersonil"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div></center>')
			i =  i+1
			data_personil.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_personil}, status=200)

		return render(request, 'personil/index.html', context={'form_personil': form, 'personil': personil})

	@csrf_exempt
	def post(self, request):
		try : 

			check_asrip = User.objects.filter(is_active=False, username=request.POST.get("username")).count()
			check_asrip_2 = User.objects.filter(is_active=False, email=request.POST.get("email")).count()
			
			if check_asrip > 0 or check_asrip_2 > 0:
				data_user_arsip = User.objects.get(Q(is_active=False) & (Q(username=request.POST.get("username")) | Q(email=request.POST.get("email"))))
				print(data_user_arsip.id)
				data = {'id': data_user_arsip.id,
						'email': data_user_arsip.email,
						'username': data_user_arsip.username,
						'nama': data_user_arsip.first_name
						}
				return JsonResponse({'msg': 'Username/Email Sudah ada pada data arsip', 'type': 'warning', 'personil': data, 'arsip': True}, status=200)
			else:
				form = PersonilForm(request.POST, request.FILES)
				if form.is_valid():
					try:
						new_personil = form.save(commit=False)
						password = new_personil.password
						new_personil.no_personil = generate_id('ES', 8)
						new_personil.set_password(password)
						new_personil.save()
						data = model_to_dict(new_personil)
						data.pop('photo')
						return JsonResponse({'personil': data, 'msg': 'Berhasil Menambah data Personil', 'type': 'success', 'arsip': False}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Personil {}'.format(e), 'type': 'error', 'arsip': False}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Personil Tidak Valid <br> {}'.format(error), 'type': 'error', 'arsip': False}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan Personil {}'.format(e), 'type': 'error', 'arsip': False}, status=400)

@method_decorator(login_required, name='post')
class PersonilDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			personil = User.objects.exclude(is_staff=True).get(id=request.POST.get("id"))
			personil.is_active = False
			personil.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Personil (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Personil (Arsip)', 'type': 'error'}, status=443)

class PersonilDetail(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		switcher = {
			"adm_gudang" : "Admin Gudang",
			"adm_outlet" : "Admin Outlet",
			"kurir" : "Kurir"
		}
		try:
			personil = User.objects.exclude(is_staff=True).exclude(role='kurir').get(id = request.GET.get("id"))
			photo = personil.photo.url if personil.photo else ''
			role = personil.role
			try :
				penempatan_toko = personil.penempatan_toko.nama_toko + ' | Alamat: ' + personil.penempatan_toko.alamat if personil.penempatan_toko else None
				penempatan_toko_id = personil.penempatan_toko.id if personil.penempatan_toko else 0

				penempatan_gudang = personil.penempatan_gudang.nama_gudang + ' | Alamat: ' + personil.penempatan_gudang.alamat if personil.penempatan_gudang else None
				penempatan_gudang_id = personil.penempatan_gudang.id if personil.penempatan_gudang else 0
			except Exception as e :
				penempatan_toko = None
				penempatan_toko_id = 0

				penempatan_gudang = None
				penempatan_gudang_id = 0

			data = {
				'id' : personil.id,
				'no_personil' : personil.no_personil,
				'first_name': personil.first_name,
				'no_telp': personil.no_telp,
				'alamat': personil.alamat,
				'email': personil.email,
				'username': personil.username,
				'role' : role,
				'photo' : photo,
				'penempatan_toko' : penempatan_toko,
				'penempatan_toko_id' : penempatan_toko_id,
				'penempatan_gudang' : penempatan_gudang,
				'penempatan_gudang_id' : penempatan_gudang_id,
			}
			
			return JsonResponse({'data': data, 'msg': 'Berhasil Mengambil Data Personil', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Personil {}'.format(e), 'type': 'error'}, status=400)
 
	@csrf_exempt
	def post(self, request):
		try: 
			obj = get_object_or_404(User, id = request.POST.get("id"))
			form = PersonilEditFormV2(request.POST, request.FILES or None, instance = obj)
			input_password = request.POST.get('password')
			input_re_password = request.POST.get('re_password')

			if form.is_valid():
				try:
					new_personil = form.save(commit=False)
					if input_password != '' and input_re_password != '': 
						if input_password == input_re_password:
							obj.set_password(input_password)
							obj.save()
						else:
							return JsonResponse({'msg': 'Password Tidak sama', 'type': 'error'}, status=200)

					new_personil.save()
					data = model_to_dict(new_personil)
					data.pop('photo')
					return JsonResponse({'msg': 'Berhasil Update data Personil', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Update data Personil {}'.format(e), 'type': 'error'}, status=400)
			else:
				error = [er[0] for er in form.errors.values()]
				error = "<br> ".join(error)
				return JsonResponse({'msg': 'Gagal Update, Form Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=400)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})

class PersonilActivate(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			personil = User.objects.exclude(is_staff=True).get(id=request.POST.get("id"))
			personil.is_active = True
			personil.save()
			return JsonResponse({'msg': 'Berhasil Merestore Personil', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=422)