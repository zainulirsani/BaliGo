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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from .pengiriman_ambil_data import *

from ekspedisi.views.custom_decorator import *

class PelangganTrackAPIView(View):
	# @method_decorator(user_customer_check(path_url='/customer/login/'))
	def get(self,request):
		try:
			id_pengiriman = request.GET.get('no_resi')
			try:
				data_pengiriman = ambil_data(get_object_or_404(Pengiriman, id_pengiriman=id_pengiriman))
				try :
					data_pengiriman.pop('qr_code')
				except :
					pass
			except Exception as e:
				return JsonResponse({'pengiriman': '', 'layanan': '', 'log_pengiriman':'', 'status_akhir': '', 'tgl_pengiriman':'', 'msg': 'RESI Tidak Ditemukan', 'type': 'warning'}, status=500)

			try:
				data_layanan = get_object_or_404(Layanan, id = data_pengiriman['id_layanan'])
			except Exception as e:
				return JsonResponse({'pengiriman': '', 'layanan': '', 'log_pengiriman':'', 'status_akhir': '', 'tgl_pengiriman':'', 'msg': 'Data Layanan Pada Order ini Tidak Ditemukan', 'type': 'warning'}, status=500)
			
			try:
				log_pengiriman = list(LogPengiriman.objects.values().filter(id_pengiriman_id=data_pengiriman['id']))
				status_akhir = LogPengiriman.objects.filter(id_pengiriman_id=data_pengiriman['id']).order_by('-id')[0]
			except Exception as e:
				return JsonResponse({'pengiriman': '', 'layanan': '', 'log_pengiriman':'', 'msg': 'Data Log_pengiriman Pada Order ini Tidak Ditemukan', 'type': 'warning'}, status=500)

			if data_pengiriman and data_layanan and log_pengiriman:
				return JsonResponse({'pengiriman': data_pengiriman, 'layanan': model_to_dict(data_layanan), 'log_pengiriman': log_pengiriman, 'status_akhir': model_to_dict(status_akhir), 'tgl_pengiriman': data_pengiriman['created_at'] if hasattr(data_pengiriman, 'created_at') else None, 'msg': 'Berhasil Mendapatkan Paket', 'type': 'success'}, status=200)
			else:
				return JsonResponse({'pengiriman': '', 'layanan': '', 'log_pengiriman': '', 'status_akhir': '', 'tgl_pengiriman': '', 'msg': 'Resi Tidak Ditemukan', 'type': 'warning'}, status=500)

		except Exception as e:
			print(e)
			return JsonResponse({'pengiriman': '', 'layanan': '', 'log_pengiriman':'', 'status_akhir': '', 'tgl_pengiriman':'', 'msg': 'Ada yg Tidak Beres, silahkan coba beberapa saat lagi', 'type': 'warning'}, status=500)