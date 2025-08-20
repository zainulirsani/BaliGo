from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, CreateView

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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from ekspedisi.views.custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class PelangganRegisterView(View):
	# @method_decorator(user_customer_check(path_url='/customer/register/'))
	def get(self,request):
		form = PelangganForm()
		data = {
			'first_name': '',
			'email': '',
			'no_telp': '',
			'alamat': '',
			'register_sebagai': 'personal',
			'username': ''
		}
		return render(request, 'frontend_pelanggan/templates/register/index.html', context={'form': form, 'data': data})

	@csrf_exempt
	def post(self, request):
		try : 
			form = PelangganForm(request.POST)
			form_pelanggan_detail = PelangganDetailInfoForm(request.POST)
			form_kosongan = PelangganForm()

			first_name = request.POST.get('first_name')
			email = request.POST.get('email')
			no_telp = request.POST.get('no_telp')
			alamat = request.POST.get('alamat')
			register_sebagai = request.POST.get('register_sebagai')
			username = request.POST.get('username')
			provinsi = request.POST.get('provinsi')
			kota = request.POST.get('kota')
			kecamatan = request.POST.get('kecamatan')
			desa = request.POST.get('desa')
			kode_pos = request.POST.get('kode_pos')

			data = {
				'first_name': first_name,
				'email': email,
				'no_telp': no_telp,
				'alamat': alamat,
				'register_sebagai': register_sebagai,
				'username': username,
				'provinsi': provinsi,
				'kota': kota,
				'kecamatan': kecamatan,
				'desa': desa,
				'kode_pos': kode_pos
			}
			if form.is_valid():
				try:
					new_pelanggan = form.save(commit=False)
					password = new_pelanggan.password
					new_pelanggan.no_personil = generate_id('CR', 8)
					new_pelanggan.set_password(password)
					new_pelanggan.is_active = False
					try :
						if form_pelanggan_detail.is_valid() :
							pelanggan_detail = form_pelanggan_detail.save(commit=False)
							new_pelanggan.save()
							pelanggan_detail.pelanggan_id_id = new_pelanggan.id
							pelanggan_detail.save()
						else :
							print(form_pelanggan_detail.errors)
							raise Exception(e)

					except Exception as e :
						print("TERJADI KESALAHAN MENYIMPAN DATA DETAIL PELANGGAN", e)
						raise Exception(e);
					# Aktivasi akun via email
					current_site = get_current_site(request)
					mail_subject = 'Activate your account.'
					message = render_to_string('frontend_pelanggan/templates/register/acc_active_email.html', {
						'user': new_pelanggan,
						'domain': current_site.domain,
						'uid': urlsafe_base64_encode(force_bytes(new_pelanggan.pk)),
						'token': default_token_generator.make_token(new_pelanggan),
						})
					to_email = form.cleaned_data.get('email')
					email = EmailMessage(
						mail_subject, message, 'no-reply@samitraexpress.id', to=[to_email]
						)
					email.send()
					#End bagian Aktivasi Email

					storage = messages.get_messages(request)
					storage.used = True
					pesan = "Sukses Melakukan Register, Silahkan Konfirmasi Email Anda."
					messages.success(request, pesan)
					return redirect('customer_login')

				except Exception as e :
					storage = messages.get_messages(request)
					storage.used = True
					pesan = "Terjadi Kesalahan {}".format(str(e))
					messages.warning(request, pesan)
					# return redirect('customer_register')
					return render(request, 'frontend_pelanggan/templates/register/index.html', context={'form': form_kosongan, 'data': data})
			else:
				error = [er[0] for er in form.errors.values()]
				error = "<br> ".join(error)
				storage = messages.get_messages(request)
				storage.used = True
				pesan = error
				messages.warning(request, pesan)
				# return redirect('customer_register')
				return render(request, 'frontend_pelanggan/templates/register/index.html', context={'form': form_kosongan, 'data': data})
		except Exception as e :
			storage = messages.get_messages(request)
			storage.used = True
			pesan = "Terjadi Kesalahan {}".format(str(e))
			messages.error(request, pesan)
			# return redirect('customer_register')
			return render(request, 'frontend_pelanggan/templates/register/index.html', context={'form': form_kosongan, 'data': data})

class PelangganRegisterActivateView(View):
	def get(self, request, uidb64, token):
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User._default_manager.get(pk=uid)
		except(TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user is not None and default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			return render(request, 'frontend_pelanggan/templates/register/complete_regis.html', context={'message': 'Thank you for your email confirmation. Now you can login your account.'})
		else:
			return render(request, 'frontend_pelanggan/templates/register/complete_regis.html', context={'message': 'Activation link is invalid!'})

class PelangganResetPassword(View):
	def get(self, request):
		data = {
			'email': ''
		}
		try:
			current_user = request.user
			data['email'] = current_user.email
		except:
			data['email'] = ''

		return render(request, 'frontend_pelanggan/templates/register/reset.html', context={'data': data})

	def post(self, request):
		data = {
			'email': request.POST.get('email'),
			'status': 'success',
			'msg': 'Silahkan cek Email anda untuk mereset password!'
		}
		try:
			email = request.POST.get('email')
			user = get_object_or_404(User, is_active=True, email=email)
			if user:
				# Reset akun via email
				current_site = get_current_site(request)
				mail_subject = 'Reset your password.'
				message = render_to_string('frontend_pelanggan/templates/register/reset_password_email.html', {
					'user': user.username,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.id)),
					'token': default_token_generator.make_token(user),
				})
				to_email = email
				email = EmailMessage(
					mail_subject, message, 'no-reply@samitraexpress.id', to=[to_email]
					)
				email.send()
				#End bagian Reset Password
				
				return JsonResponse(data, status=200)

			else:
				data['status'] = 'error'
				data['msg'] = 'Akun dengan Alamat email ini tidak ditemukan!'
				return JsonResponse(data, status=422)

		except Exception as e:
			data['status'] = 'error'
			data['msg'] = '[Terjadi Kesalahan], {}'.format(e)

			return JsonResponse(data, status=422)

class PelangganResetPasswordActionView(View):
	def get(self, request, uidb64, token):
		try:
			uid = urlsafe_base64_decode(uidb64).decode()
			user = User._default_manager.get(pk=uid)
		except(TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user is not None and default_token_generator.check_token(user, token):
			user_id = user.id
			user_email = user.email
			return render(request, 'frontend_pelanggan/templates/register/form_reset.html', context={'user_id': user_id, 'user_email': user_email})
		else:
			return render(request, 'frontend_pelanggan/templates/register/form_reset.html', context={'user_id': '', 'user_email': ''})

class PelangganResetPasswordAction2View(View):
	def post(self, request):
		try:
			id_user = request.POST.get('id')
			email_user = request.POST.get('email')
			password1 = request.POST.get('password1')
			password2 = request.POST.get('password2')
			url_redirect = ''

			if password1 == password2:
				user = get_object_or_404(User, is_active=True, id=id_user)
				user.set_password(password1)
				user.save()
				if user.register_sebagai is not None:
					url_redirect = reverse('customer_login')
				elif user.role == 'kurir':
					url_redirect = reverse('kurir_login')
				else:
					url_redirect = reverse('login')

			else:
				return JsonResponse({'msg': 'Password Salah!', 'type': 'error', 'url': url_redirect}, status=422)
				# return render(request, 'frontend_pelanggan/templates/register/complete_reset.html', context={'message': 'Password salah!'})

			return JsonResponse({'msg': 'Sukses Mereset Password Silahkan Login kembali.', 'type': 'success', 'url': url_redirect}, status=422)
			# return render(request, 'frontend_pelanggan/templates/register/complete_reset.html', context={'message': 'Sukses Mereset Password Silahkan Login kembali.'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mereset Password {}'.format(e), 'type': 'success', 'url': url_redirect}, status=422)
			# return render(request, 'frontend_pelanggan/templates/register/complete_reset.html', context={'message': 'Gagal Mereset Password {}'.format(e)})