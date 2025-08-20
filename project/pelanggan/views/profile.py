from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime
from random import randint

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from ekspedisi.models import *
from ekspedisi.forms import *

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission

from ekspedisi.views.custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

def check_data_update(data_username, data_email, id):
	try:
		data_user = list(User.objects.exclude(id=id).values())
		for user in data_user:
			if data_username.lower() == user['username'].lower():
				pass
				return False, 'Username Sudah Digunakan'
			if data_email.lower() == user['email'].lower():
				pass
				return False, 'Email Sudah Digunakan'
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
	data['username'] = user_update.username
	data['name'] = user_update.first_name
	data['no_hp'] = user_update.no_telp
	data['alamat'] = user_update.alamat
	data['url_photo'] = user_update.photo.name
	data['email'] = user_update.email
	
@method_decorator(login_required(login_url='/login'), name='get')
class PelangganProfileView(View):
	# @method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self,request):
		if request.user.is_authenticated:
			data = {
				'id': request.user.id,
				'username': request.user.username,
				'name': request.user.first_name,
				'no_hp': request.user.no_telp,
				'alamat': request.user.alamat,
				'url_photo': request.user.photo.name,
				'email': request.user.email,
				'provinsi': request.user.pelanggan_detail.provinsi_id if hasattr(request.user, 'pelanggan_detail') else 0,
				'kota': request.user.pelanggan_detail.kota_id if hasattr(request.user, 'pelanggan_detail') else 0,
				'kecamatan': request.user.pelanggan_detail.kecamatan_id if hasattr(request.user, 'pelanggan_detail') else 0,
				'desa': request.user.pelanggan_detail.desa_id if hasattr(request.user, 'pelanggan_detail') else 0,
				'kode_pos': request.user.pelanggan_detail.kode_pos_id if hasattr(request.user, 'pelanggan_detail') else 0,

			}
			
		else:
			data = {
				'id': '',
				'username': '',
				'name': '',
				'no_hp': '',
				'alamat': '',
				'url_photo': '',
				'email': '',
				'provinsi': '',
				'kota':'',
				'kecamatan':'',
				'desa':'',
				'kode_pos':''	
			}
		return render(request, 'frontend_pelanggan/templates/profile/index.html', {'data': data})

	def post(self, request):
		id_ = request.POST.get('id')
		nama_ = request.POST.get('name')
		alamat_ = request.POST.get('alamat')
		no_telp_ = request.POST.get('no_hp')
		password1_ = request.POST.get('password')
		password2_ = request.POST.get('re_password')

		pesan =''
		type_pesan = ''
		data = {
			'id': '',
			'username': '',
			'name': '',
			'no_hp': '',
			'alamat': '',
			'url_photo': '',
			'email': '',
		}

		try:
			print("USERID", id_)
			user = get_object_or_404(User, id=id_)
			user.first_name = nama_
			user.alamat = alamat_
			user.no_telp = no_telp_
			if password1_ != '' and password2_ != '':
				if password1_ == password2_:
					user.set_password(password1_)
					user.save()
					user_update = get_object_or_404(User, id=id_)
					set_value_data(data, user_update)

					try :
						user_id = InformasiPelanggan.objects.get(pelanggan_id=id_)
						form_pelanggan_detail = PelangganDetailInfoForm(request.POST or None, instance=user_id)
						if form_pelanggan_detail.is_valid() :
							pelanggan_detail = form_pelanggan_detail.save(commit=False)
							pelanggan_detail.pelanggan_id_id = user.id
							pelanggan_detail.save()
						else :
							print("ADA ERROR", form_pelanggan_detail.errors)
							pass

					except :
						pass
					storage = messages.get_messages(request)
					storage.used = True
					pesan = "Berhasil Mengupdate Profile & Password"
					messages.success(request, pesan)
					
				else:
					user_update = get_object_or_404(User, id=id_)
					set_value_data(data, user_update)

					storage = messages.get_messages(request)
					storage.used = True
					pesan = "Password Tidak Sama"
					messages.warning(request, pesan)
					
			else:
				user.save()
				user_update = get_object_or_404(User, id=id_)
				set_value_data(data, user_update)
				storage = messages.get_messages(request)
				storage.used = True
				pesan = "Berhasil Mengupdate Profile"
				try :
					user_id = InformasiPelanggan.objects.get(pelanggan_id=id_)
					form_pelanggan_detail = PelangganDetailInfoForm(request.POST or None, instance=user_id)
					if form_pelanggan_detail.is_valid() :
						pelanggan_detail = form_pelanggan_detail.save(commit=False)
						pelanggan_detail.pelanggan_id_id = user.id
						pelanggan_detail.save()
					else :
						print("ADA ERROR", form_pelanggan_detail.errors)
						pass

				except :
					pass
				messages.success(request, pesan)
			data['provinsi'] = request.POST.get('provinsi', 0)
			data['kota'] = request.POST.get('kota', 0)
			data['kecamatan'] = request.POST.get('kecamatan', 0)
			data['desa'] = request.POST.get('desa', 0)
			data['kode_pos'] = request.POST.get('kode_pos', 0)

			return render(request, 'frontend_pelanggan/templates/profile/index.html', {'data': data})
		except Exception as e:
			user_update = get_object_or_404(User, id=id_)
			set_value_data(data, user_update)
			return render(request, 'frontend_pelanggan/templates/profile/index.html', {'data': data})