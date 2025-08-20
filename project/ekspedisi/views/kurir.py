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

class KurirView(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request):

		form = KurirForm()

		if request.user.is_authenticated:
			is_admin = request.user.is_superuser
		else:
			is_admin = False

		if is_admin:
			kurir = list(User.objects.filter(Q(role='kurir')).select_related('personil_toko').values())
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
				kurir = list(User.objects.filter(Q(role='kurir') & Q(penempatan_toko_id=outlet_tugas)).select_related('personil_toko').values())
			elif is_gudang:
				kurir = list(User.objects.filter(Q(role='kurir') & Q(penempatan_gudang_id=gudang_tugas)).select_related('personil_toko').values())

		data_list = []
		data_kurir = []
		i = 1
		for data in kurir:
			data_list = [i]
			data_list.append(data['no_personil'])
			data_list.append(data['first_name'])
			data_list.append(data['email'])
			data_list.append(data['no_telp'])
			data_list.append(data['alamat'])

			if data['penempatan_toko_id']:
				data_toko = model_to_dict(get_object_or_404(Toko, id = data['penempatan_toko_id']))
				data_list.append('Outlet: ' + data_toko['nama_toko'])
			elif data['penempatan_gudang_id']:
				data_gudang = model_to_dict(get_object_or_404(Gudang, id = data['penempatan_gudang_id']))
				data_list.append('Gudang: ' + data_gudang['nama_gudang'])
			else:
				data_list.append('Kosong')

			if is_admin:
				btn_delete = '<a href="javascript:void(0)" data-toggle="tooltip" title="Delete Kurir" data-id="' + str(data['id']) + '" data-nama="' + str(data['first_name']) + '"class="btn btn-danger btn-sm deleteKurir"><i class="fa fa-fw fa-trash-alt"></i></a>'
			else:
				btn_delete = ''

			if data['is_active'] == True:
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Arsipkan Kurir" data-id="' + str(data['id']) + '" data-nama="' + str(data['first_name']) + '"class="btn btn-warning btn-sm arsipKurir"><i class="fa fa-fw fa-archive"></i></a>'
			else:
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Kembalikan Kurir" data-id="' + str(data['id']) + '" data-nama="' + str(data['first_name']) + '"class="btn btn-success btn-sm unarsipKurir"><i class="fa fa-fw fa-upload"></i></a>'

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Edit Kurir" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editKurir"><i class="fa fa-fw fa-edit"></i></a>' + btn_arsip + btn_delete + '</div></center>')
			i =  i+1
			data_kurir.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_kurir}, status=200)

		return render(request, 'kurir/index.html', context={'form': form, 'kurir': data_kurir})

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
				return JsonResponse({'msg': 'Username/EmailSudah ada pada data arsip', 'type': 'warning', 'personil': data, 'arsip': True}, status=200)
			else:
				form = KurirForm(request.POST, request.FILES)
				if form.is_valid():
					try:
						new_kurir = form.save(commit=False)
						password = new_kurir.password
						new_kurir.no_personil = generate_id('ES', 8)
						new_kurir.set_password(password)
						new_kurir.save()
						data = model_to_dict(new_kurir)
						data.pop('photo')
						return JsonResponse({'kurir': data, 'msg': 'Berhasil Menambah data Kurir', 'type': 'success', 'arsip': False}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data Kurir {}'.format(e), 'type': 'error', 'arsip': False}, status=422)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form Kurir Tidak Valid <br> {}'.format(error), 'type': 'error', 'arsip': False}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan Kurir {}'.format(e), 'type': 'error', 'arsip': False}, status=400)

class KurirDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			kurir = User.objects.get(id=request.POST.get('id'))
			kurir.delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Kurir', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data Kurir', 'type': 'error'}, status=422)

class KurirArsip(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			kurir = User.objects.get(id=request.POST.get('id'))
			kurir.is_active = False
			kurir.save()
			return JsonResponse({'msg': 'Berhasil Mengarsipkan Data Kurir', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengarsipkan Data Kurir', 'type': 'error'}, status=422)

class KurirUnarsip(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			kurir = User.objects.get(id=request.POST.get('id'))
			kurir.is_active = True
			kurir.save()
			return JsonResponse({'msg': 'Berhasil mengembalikan Data Kurir', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal mengembalikan Data Kurir', 'type': 'error'}, status=422)


class KurirDetail(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			kurir = User.objects.get(id = request.GET.get('id'))
			photo = kurir.photo.url if kurir.photo else ''
			if kurir.penempatan_gudang:
				data_gudang = kurir.penempatan_gudang.nama_gudang
				id_gudang = kurir.penempatan_gudang.id
				alamat_gudang = kurir.penempatan_gudang.alamat
			else:
				data_gudang = ''
				id_gudang = ''
				alamat_gudang = ''

			if kurir.penempatan_toko:
				data_toko = kurir.penempatan_toko.nama_toko
				id_toko = kurir.penempatan_toko.id
				alamat_toko = kurir.penempatan_toko.alamat
			else:
				data_toko = ''
				id_toko = ''
				alamat_toko = ''
			
			data = {
				'id': kurir.id,
				'no_personil': kurir.no_personil,
				'first_name': kurir.first_name,
				'no_telp': kurir.no_telp,
				'alamat': kurir.alamat,
				'email': kurir.email,
				'username': kurir.username,
				'nama_gudang': data_gudang + ' | Alamat: ' + alamat_gudang,
				'id_gudang': id_gudang,
				'nama_toko': data_toko + ' | Alamat: ' + alamat_toko,
				'id_toko': id_toko,
				'photo' : photo
			}
			
			return JsonResponse({'data': data, 'msg': 'Berhasil Mengambil Data Kurir', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Kurir {}'.format(e), 'type': 'error'})

	def post(self, request):
		try: 
			obj = get_object_or_404(User, id = request.POST.get('id'))
			form = KurirFormEdit(request.POST, request.FILES or None, instance = obj)
			input_password = request.POST.get('password')
			input_re_password = request.POST.get('re_password')

			if form.is_valid():
				try:
					new_kurir = form.save(commit=False)
					if input_password != '' and input_re_password != '':
						if input_password == input_re_password:
							obj.set_password(input_password)
							obj.save()
						else:
							return JsonResponse({'msg': 'Password Tidak sama', 'type': 'error'}, status=200)
					new_kurir.save()
					data = model_to_dict(new_kurir)
					data.pop('photo')
					return JsonResponse({'msg': 'Berhasil Update data Kurir', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Menambah data kurir {}'.format(e), 'type': 'error'}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Update data Kurir Form Tidak Valid', 'type': 'error'})
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})

class KurirActivate(View):
	def post(self, request):
		try:
			kurir = User.objects.exclude(is_staff=True).get(id=request.POST.get("id"))
			kurir.is_active = True
			kurir.save()
			return JsonResponse({'msg': 'Berhasil Merestore Kurir', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=422)

class KurirListByOutlet(View):
	def get(self, request):

		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET['page'])
			outlet_tugas = request.GET['outlet']
			total_counts = User.objects.filter(Q(is_active=True) & Q(role='kurir') & Q(penempatan_toko_id=outlet_tugas) & (Q(username__icontains=q) | Q(first_name__icontains=q))).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(User.objects.values().filter(Q(is_active=True) & Q(role='kurir') & Q(penempatan_toko_id=outlet_tugas) & (Q(username__icontains=q) | Q(first_name__icontains=q)))[start_p:pages])
			
		else:
			page = int(request.GET['page'])
			outlet_tugas = request.GET['outlet']
			total_counts = User.objects.filter(Q(is_active = True) & Q(role='kurir') & Q(penempatan_toko_id=outlet_tugas)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0
				
			datas = list(User.objects.values().filter(Q(is_active = True) & Q(role='kurir') & Q(penempatan_toko_id=outlet_tugas))[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': (data['first_name'] + " || " + data['username'])})
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)