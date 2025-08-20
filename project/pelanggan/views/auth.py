from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime
from random import randint

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from ekspedisi.models import *
from ekspedisi.forms import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission

""" AUNTENTICATE """


def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class PelangganLoginView(View) :
	def get(self, request):
		if request.user and request.user.is_authenticated :
			return redirect('customer_home');
		return render(request, 'frontend_pelanggan/templates/auth/login.html', {})

	def post(self, request) :
		try :
			username = request.POST.get('username')
			password = request.POST.get('password')
			if username and password:
				check_user = User.objects.get(username=username)

				if check_user.is_active == True:
					user = authenticate(username=username, password=password)
					if user :
						if user.register_sebagai and user.is_active == True and user.is_superuser == False and user.role is None:
							auth_login(request, user)
							return redirect('customer_home')
						else :
							storage = messages.get_messages(request)
							storage.used = True
							pesan = "Hanya diizinkan untuk akun Pelanggan"
							messages.warning(request, pesan)
					else :
						storage = messages.get_messages(request)
						storage.used = True
						pesan = "Username atau password salah"
						messages.warning(request, pesan)
				else:
					storage = messages.get_messages(request)
					storage.used = True
					pesan = "Ups, Akun anda belum aktif."
					messages.warning(request, pesan)
		except Exception as e :
			storage = messages.get_messages(request)
			storage.used = True
			pesan = "Terjadi Kesalahan {}".format(str(e))
			messages.warning(request, pesan)
		return redirect('customer_login')


def PelangganLogout(request) : 
	auth_logout(request)
	return redirect('customer_login')
""" END AUTHENTICATE """