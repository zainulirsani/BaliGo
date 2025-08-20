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
from django.db.models.functions import Lower, Concat


from .custom_decorator import *
from django.db.models import Q, Count, Sum

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

@method_decorator(login_required(login_url='/admin'), name='get')
class DashboardView(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self,request):
		search_type = request.GET.get('type')
		search_term = request.GET.get('search')

		try:
			total_pelanggan = User.objects.filter((Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company'))).count()
			# if request.user.is_staff : 
			# 	# Mencari Outlet pengiriman yang dilewati untuk pelanggan pengiriman
			# 	if(search_type and search_type.lower() == 'outlet') :
			# 		total_pelanggan_telp = list(Pengiriman.objects.filter(outlet_pengiriman__nama_toko=search_term).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('no_telp_pengirim', flat=True))
			# 		total_pelanggan_nama = list(Pengiriman.objects.filter(outlet_pengiriman__nama_toko=search_term).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('nama_pengirim', flat=True))
			# 		total_pelanggan = len(list(User.objects.values().filter(Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company'), no_telp__in=total_pelanggan_telp, first_name__in=total_pelanggan_nama)))
			# 		# pengiriman_nama = Pengiriman.objects.filter(is_active=True, outlet_pengiriman__nama_toko=search_term).annotate(name_lower=Lower('nama_pengirim'))
			# 		# pengiriman_nama = list(pengiriman_nama.values('name_lower', 'no_telp_pengirim').distinct())
			# 		# total_pelanggan = len(pengiriman_nama)
			# 	# Mencari gudang pengiriman yang dilewati untuk pelanggan pengiriman
			# 	if(search_type and search_type.lower() == 'gudang') :
			# 		total_pelanggan_telp = list(Pengiriman.objects.filter(gudang_pengiriman__nama_gudang=search_term).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('no_telp_pengirim', flat=True))
			# 		total_pelanggan_nama = list(Pengiriman.objects.filter(gudang_pengiriman__nama_gudang=search_term).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('nama_pengirim', flat=True))
			# 		total_pelanggan = len(list(User.objects.values().filter(Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company'), no_telp__in=total_pelanggan_telp, first_name__in=total_pelanggan_nama)))
			# 		# pengiriman_nama = Pengiriman.objects.filter(is_active=True, gudang_pengiriman__nama_gudang=search_term).annotate(name_lower=Lower('nama_pengirim'))
			# 		# pengiriman_nama = list(pengiriman_nama.values('name_lower', 'no_telp_pengirim').distinct())
					# total_pelanggan = len(pengiriman_nama)

			# elif hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				# total_pelanggan_telp = list(Pengiriman.objects.filter(outlet_pengiriman_id=request.user.penempatan_toko_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('no_telp_pengirim', flat=True))
				# total_pelanggan_nama = list(Pengiriman.objects.filter(outlet_pengiriman_id=request.user.penempatan_toko_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('nama_pengirim', flat=True))
				# total_pelanggan = len(list(User.objects.values().filter(Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company'), no_telp__in=total_pelanggan_telp, first_name__in=total_pelanggan_nama)))

			# elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				# total_pelanggan_telp = list(Pengiriman.objects.filter(gudang_pengiriman_id=request.user.penempatan_gudang_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('no_telp_pengirim', flat=True))
				# total_pelanggan_nama = list(Pengiriman.objects.filter(gudang_pengiriman_id=request.user.penempatan_gudang_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('nama_pengirim', flat=True))
				# total_pelanggan = len(list(User.objects.values().filter(Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company'), no_telp__in=total_pelanggan_telp, first_name__in=total_pelanggan_nama)))
			
		except Exception as e:
			print(e)
			total_pelanggan = 0

		try:
			if request.user.is_staff : 
				total_kurir = User.objects.filter(is_active=True, role='kurir').count()
				# Mencari Outlet untuk penempatan Kurir
				if(search_type and search_type.lower() == 'outlet') :
					penempatan_kurir = User.objects.filter(is_active=True, role='kurir', penempatan_toko__nama_toko=search_term).count()
					total_kurir = penempatan_kurir
				# Mencari gudang  untuk penempatan Kurir
				if(search_type and search_type.lower() == 'gudang') :
					penempatan_gudang = User.objects.filter(is_active=True, role='kurir', penempatan_gudang__nama_gudang=search_term).count()
					total_kurir = penempatan_gudang
			elif hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				total_kurir = User.objects.filter(is_active=True, role='kurir', penempatan_toko_id=request.user.penempatan_toko_id).count()
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				total_kurir = User.objects.filter(is_active=True, role='kurir', penempatan_gudang_id=request.user.penempatan_gudang_id).count()

		except Exception as e:
			total_kurir = 0
		# print(total_kurir)
		try:
			if request.user.is_staff :
				total_kendaraan = Kendaraan.objects.filter(is_active=True).count()
				# Mencari Outlet ntuk total kendaraan
				if(search_type and search_type.lower() == 'outlet') :
					kendaraan_toko = Kendaraan.objects.filter(is_active=True, penempatan_toko__nama_toko=search_term).count()
					total_kendaraan = kendaraan_toko
				# Mencari gudang untuk total kendaraan
				if(search_type and search_type.lower() == 'gudang') :
					kendaraan_gudang = Kendaraan.objects.filter(is_active=True, penempatan_gudang__nama_gudang=search_term).count()
					total_kendaraan = kendaraan_gudang
			elif hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				total_kendaraan = Kendaraan.objects.filter(is_active=True, penempatan_toko_id=request.user.penempatan_toko_id).count()
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				total_kendaraan = Kendaraan.objects.filter(is_active=True, penempatan_gudang_id=request.user.penempatan_gudang_id).count()
		except Exception as e:
			total_kendaraan = 0

		try:
			if request.user.is_staff : 
				total_pengiriman = Pengiriman.objects.filter(Q(is_active=True) & ~Q(log_pengiriman__status_pengiriman__in=('done',))).distinct().values().count()
				# Mencari Outlet ntuk total kendaraan
				if(search_type and search_type.lower() == 'outlet') :
					pengiriman_toko = Pengiriman.objects.filter(Q(is_active=True) & ~Q(log_pengiriman__status_pengiriman__in=('done',)), outlet_pengiriman__nama_toko=search_term).count()
					total_pengiriman = pengiriman_toko
				# Mencari gudang untuk total kendaraan
				if(search_type and search_type.lower() == 'gudang') :
					pengiriman_gudang = Pengiriman.objects.filter(Q(is_active=True) & ~Q(log_pengiriman__status_pengiriman__in=('done',)), gudang_pengiriman__nama_gudang=search_term).count()
					total_pengiriman = pengiriman_gudang
			elif hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				total_pengiriman = Pengiriman.objects.filter(Q(is_active=True) & ~Q(log_pengiriman__status_pengiriman__in=('done',)) & Q(Q(log_pengiriman__id_kurir__penempatan_toko_id=request.user.penempatan_toko_id) | Q(outlet_pengiriman_id=request.user.penempatan_toko_id))).order_by("-pk").distinct().values().count()
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				total_pengiriman = Pengiriman.objects.filter(Q(is_active=True) & ~Q(log_pengiriman__status_pengiriman__in=('done',)) & Q(log_pengiriman__id_kurir__penempatan_gudang_id=request.user.penempatan_gudang_id)).order_by("-pk").distinct().values().count()
		except Exception as e:
			total_pengiriman = 0
		print("TOTAL PENGIRIMAN AKTIF", total_pengiriman)

		try:
			if request.user.is_staff : 
				total_pengiriman_selesai = LogPengiriman.objects.filter(Q(id_pengiriman__is_active=True) & Q(status_pengiriman = 'done')).values('id_pengiriman_id', 'status_pengiriman').distinct().count()
				# Mencari Outlet ntuk total kendaraan
				if(search_type and search_type.lower() == 'outlet') :
					toko_done = LogPengiriman.objects.filter(Q(id_pengiriman__is_active=True) & Q(status_pengiriman = 'done') & Q(rute_pengiriman_outlet__nama_toko=search_term)).values('id_pengiriman_id', 'status_pengiriman').distinct().count()
					total_pengiriman_selesai = toko_done
				# Mencari gudang untuk total kendaraan
				if(search_type and search_type.lower() == 'gudang') :
					gudang_done = LogPengiriman.objects.filter(Q(id_pengiriman__is_active=True) & Q(status_pengiriman = 'done') & Q(rute_pengiriman_gudang__nama_gudang=search_term)).values('id_pengiriman_id', 'status_pengiriman').distinct().count()
					total_pengiriman_selesai = gudang_done
			elif hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				data_log =  LogPengiriman.objects.filter(Q(Q(id_kurir__penempatan_toko_id=request.user.penempatan_toko_id) | Q(id_pengiriman__outlet_pengiriman_id=request.user.penempatan_toko_id)), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
				total_pengiriman_selesai = Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').count()
				# total_pengiriman_selesai = LogPengiriman.objects.filter(Q(status_pengiriman = 'done') & Q(Q(id_kurir__penempatan_toko_id=request.user.penempatan_toko_id) | Q(id_pengiriman__outlet_pengiriman_id=request.user.penempatan_toko_id))).values('id_pengiriman_id', 'status_pengiriman').distinct().count()
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				# total_pengiriman_selesai = LogPengiriman.objects.filter(Q(id_kurir__penempatan_gudang_id=request.user.penempatan_gudang_id) & Q(status_pengiriman='done')).values('id_pengiriman_id', 'status_pengiriman').distinct().count()
				data_log =  LogPengiriman.objects.filter(Q(id_kurir__penempatan_gudang_id=request.user.penempatan_gudang_id), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
				total_pengiriman_selesai = Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').count()
		except Exception as e:
			total_pengiriman_selesai = 0

		data = {
			'pelanggan': total_pelanggan,
			'kurir': total_kurir,
			'kendaraan': total_kendaraan,
			'pengiriman': total_pengiriman,
			'pengiriman_selesai': total_pengiriman_selesai
		}
		

		return render(request, 'dashboard/index.html', context={'total': data})