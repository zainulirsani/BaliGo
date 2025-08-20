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
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission

from .custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

def check_data_update(data_username, data_email, id):
	try:
		if User.objects.exclude(id=id).filter(Q(username__icontains=data_username)).exists():
			return False, 'Username Sudah Digunakan'

		elif User.objects.exclude(id=id).filter(Q(email__icontains=data_email)).exists():
			return False, 'Email Sudah Digunakan'
		else:
			return True, ''
	except:
		return True, ''

def check_password_update(pass1, pass2):
	try:
		if pass1 or pass2:
			if pass1 == pass2:
				return True, ''
			else:
				return False, 'Password Tidak Sama!'
		else:
			return False, ''
	except:
		return False, ''

def set_value_data(data, user_update):
	data['id'] = user_update.id
	data['is_admin'] = user_update.is_superuser
	data['username'] = user_update.username
	data['no_personil'] = user_update.no_personil
	data['name'] = user_update.first_name
	data['no_hp'] = user_update.no_telp
	data['alamat'] = user_update.alamat
	data['url_photo'] = user_update.photo.name
	data['email'] = user_update.email
	data['role'] = user_update.role
	
@method_decorator(login_required(login_url='/mobile_kurir'), name='get')
class ProfileView(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self,request):
		if request.user.is_authenticated:
			profileForm = ProfileUploadPhoto()
			data = {
				'id': request.user.id,
				'is_admin': request.user.is_superuser,
				'username': request.user.username,
				'no_personil': request.user.no_personil,
				'name': request.user.first_name,
				'no_hp': request.user.no_telp,
				'alamat': request.user.alamat,
				'url_photo': request.user.photo.name,
				'email': request.user.email,
				'role' : request.user.role,
				'gudang': request.user.penempatan_gudang_id,
				'toko': request.user.penempatan_toko_id
			}

			if request.user.penempatan_toko_id:
				obj_toko = Toko.objects.get(id=request.user.penempatan_toko_id);
				penempatan = {
					'nama': obj_toko.nama_toko,
					'alamat': obj_toko.alamat,
				}
			elif request.user.penempatan_gudang_id:
				obj_gudang = Gudang.objects.get(id=request.user.penempatan_gudang_id);
				penempatan = {
					'nama': obj_gudang.nama_gudang,
					'alamat': obj_gudang.alamat,
				}
			else:
				penempatan = {
					'nama': '',
					'alamat': '',
				}
		else:
			data = {
				'id': '',
				'is_admin': '',
				'username': '-',
				'no_personil': '-',
				'name': '-',
				'no_hp': '-',
				'alamat': '-',
				'url_photo': '-',
				'email': '-',
				'role' : '-',
			}
			penempatan = {
				'nama': '',
				'alamat': '',
			}
		return render(request, 'profile/index.html', {'data': data, 'penempatan': penempatan, 'profileForm':profileForm})

	def post(self, request):
		id_ = request.POST.get('id')
		if request.is_ajax() and request.POST.get('edit-photo') :
			if request.FILES.get('photo') :
				user = get_object_or_404(User, id=id_)
				formUpload = ProfileUploadPhoto(request.POST, request.FILES, instance=user)
				if formUpload.is_valid() :
					formUpload.save()
					return JsonResponse({'msg': 'Berhasil mengubah foto profil', 'type': 'success'}, status=200)
				else :
					return JsonResponse({'msg': 'Terjadi kesalahan, form tidak valid', 'type': 'error'}, status=402)
			else :
				return JsonResponse({'msg': 'Tidak dapat memproses foto yang kosong', 'type': 'error'}, status=402)


		nama_ = request.POST.get('name')
		username_ = request.POST.get('username')
		email_ = request.POST.get('email')
		alamat_ = request.POST.get('alamat')
		no_telp_ = request.POST.get('no_hp')
		password1_ = request.POST.get('password1')
		password2_ = request.POST.get('password2')

		pesan =''
		type_pesan = ''
		data = {
			'id': '',
			'is_admin': '',
			'username': '',
			'no_personil': '',
			'name': '',
			'no_hp': '',
			'alamat': '',
			'url_photo': '',
			'email': '',
			'role' : '',
		}

		status_cek, msg = check_data_update(username_, email_, id_)
		if status_cek == True:
			try:
				user = get_object_or_404(User, id=id_)
				user.first_name = nama_
				user.username = username_
				user.email = email_
				user.alamat = alamat_
				if not user.is_superuser :
					if not no_telp_ :
						return JsonResponse({'msg': 'No Telp Wajib diisi', 'type': 'warning'}, status=422)
					elif not alamat_ :
						return JsonResponse({'msg': 'Alamat wajib diisi', 'type': 'warning'}, status=422)
					elif not nama_ :
						return JsonResponse({'msg': 'Nama personil wajib diisi', 'type': 'warning'}, status=422)

				user.no_telp = no_telp_
				if password1_ != '' and password2_ != '':
					if password1_ == password2_:
						user.set_password(password1_)
						user.save()
						user_update = get_object_or_404(User, id=id_)
						set_value_data(data, user_update)
						pesan = 'Berhasil Mengupdate Profile & Password'
						type_pesan = 'success'
					else:
						user_update = get_object_or_404(User, id=id_)
						set_value_data(data, user_update)
						pesan = 'Password dan Konfirmasi Tidak Sama'
						type_pesan = 'error'
				elif password1_ and password2_ == '' :
					return JsonResponse({'msg': 'Konfirmasi password harus diisi jika mengubah password', 'type': 'warning'}, status=422)
				else:
					user.save()
					user_update = get_object_or_404(User, id=id_)
					set_value_data(data, user_update)
					pesan = 'Berhasil Mengupdate Profile'
					type_pesan = 'success'
			except Exception as e:
				user_update = get_object_or_404(User, id=id_)
				set_value_data(data, user_update)

				return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error', 'data': data}, status=422)
		else:
			user_update = get_object_or_404(User, id=id_)
			set_value_data(data, user_update)
			pesan = msg
			type_pesan = 'error'

		return JsonResponse({'msg': pesan, 'type': type_pesan, 'data': data}, status=200)