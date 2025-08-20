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
from django.db.models import Q, Count, Sum

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

@method_decorator(login_required(login_url='/mobile_kurir'), name='get')
class KurirDashboardView(View):
	def get(self,request):
		total_order = 0
		total_order_selesai = 0
		total_pengiriman_aktif = 0
		total_pengiriman_selesai = 0
		try :
			if hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				total_order = OrderPickup.objects.filter(id_toko_id=request.user.penempatan_toko_id, is_active=True, status__in=('waiting', 'pickup')).count()
				total_order_selesai = OrderPickup.objects.filter(id_toko_id=request.user.penempatan_toko_id, is_active=False, status__in=['done']).count()
				# total_pengiriman_selesai = Pengiriman.objects.filter(log_pengiriman__status_pengiriman='done').count()
				# total_pengiriman_aktif = Pengiriman.objects.filter(outlet_pengiriman_id=request.user.penempatan_toko_id).exclude(log_pengiriman__status_pengiriman='done').count()
				total_pengiriman_aktif = Pengiriman.objects.filter(Q(is_active=True) & ~Q(log_pengiriman__status_pengiriman__in=('done',)) & Q(Q(log_pengiriman__id_kurir__penempatan_toko_id=request.user.penempatan_toko_id) | Q(outlet_pengiriman_id=request.user.penempatan_toko_id))).order_by("-pk").distinct().values().count()
				data_log =  LogPengiriman.objects.filter(Q(Q(id_kurir__penempatan_toko_id=request.user.penempatan_toko_id) | Q(id_pengiriman__outlet_pengiriman_id=request.user.penempatan_toko_id)), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
				total_pengiriman_selesai = Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').count()
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				total_order = OrderPickup.objects.filter(id_gudang_id=request.user.penempatan_gudang_id, is_active=True, status__in=('waiting', 'pickup')).count()
				total_order_selesai = OrderPickup.objects.filter(id_toko_id=request.user.penempatan_gudang_id, is_active=False, status__in=['done']).count()

				# total_pengiriman_selesai = Pengiriman.objects.filter(log_pengiriman__status_pengiriman='done').count()
				# total_pengiriman_aktif = Pengiriman.objects.filter(gudang_pengiriman_id=request.user.penempatan_gudang_id).exclude(log_pengiriman__status_pengiriman='done').count()
				total_pengiriman_aktif = Pengiriman.objects.filter(Q(is_active=True) & ~Q(log_pengiriman__status_pengiriman__in=('done',)) & Q(log_pengiriman__id_kurir__penempatan_gudang_id=request.user.penempatan_gudang_id)).order_by("-pk").distinct().values().count()
				data_log =  LogPengiriman.objects.filter(Q(id_kurir__penempatan_gudang_id=request.user.penempatan_gudang_id), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
				total_pengiriman_selesai = Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').count()
		except Exception as e: 	
			print(e)
			pass
			
		return render(request, 'mobile_kurir/templates/dashboard/index.html', {
			'is_active_dashboard': 'active',
			'total_order' : total_order,
			'total_order_selesai' : total_order_selesai,
			'total_pengiriman_aktif' : total_pengiriman_aktif,
			'total_pengiriman_selesai' : total_pengiriman_selesai
		})

@method_decorator(login_required(login_url='/mobile_kurir'), name='get')
class KurirDashboardDetailView(View) :
	def get(self, request) :
		detail_dipilih = request.GET.get('q', 'Dashboard')
		data_log = []
		switcher = {
			'order_aktif': "Order Aktif",
			'order_selesai': "Order Selesai",
			'pengiriman_aktif': "Pengiriman Aktif",
			'pengiriman_selesai': 'Pengiriman Selesai'
		}
		title = switcher.get(detail_dipilih, "")
		if(title and title == 'Order Aktif') :
			if hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				data_log = OrderPickup.objects.filter(id_toko_id=request.user.penempatan_toko_id, is_active=True, status__in=('waiting', 'pickup'))
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				data_log = OrderPickup.objects.filter(id_gudang_id=request.user.penempatan_gudang_id, is_active=True, status__in=('waiting', 'pickup'))
		elif(title and title == 'Order Selesai') :
			if hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				data_log = OrderPickup.objects.filter(id_toko_id=request.user.penempatan_toko_id, is_active=False, status='done')
				print(data_log)
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				data_log = OrderPickup.objects.filter(id_toko_id=request.user.penempatan_gudang_id, is_active=False, status='done')
		elif(title and title == 'Pengiriman Selesai') :
			if hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				# data_log = Pengiriman.objects.filter(outlet_pengiriman_id=request.user.penempatan_toko_id).exclude(log_pengiriman__status_pengiriman='done')
				data_log =  LogPengiriman.objects.filter(Q(Q(id_kurir__penempatan_toko_id=request.user.penempatan_toko_id) | Q(id_pengiriman__outlet_pengiriman_id=request.user.penempatan_toko_id)), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
				data_log = Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').order_by('-pk').distinct()
				
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				# data_log = Pengiriman.objects.filter(gudang_pengiriman_id=request.user.penempatan_gudang_id).exclude(log_pengiriman__status_pengiriman='done')
				data_log =  LogPengiriman.objects.filter(Q(id_kurir__penempatan_gudang_id=request.user.penempatan_gudang_id), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
				data_log = Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').order_by('-pk').distinct()
		elif(title and title == 'Pengiriman Aktif') :
			if hasattr(request.user, 'penempatan_toko_id') and request.user.penempatan_toko_id :
				# data_log = Pengiriman.objects.filter(log_pengiriman__status_pengiriman='done')
				data_log = Pengiriman.objects.filter(Q(is_active=True) & Q(Q(log_pengiriman__id_kurir__penempatan_toko_id=request.user.penempatan_toko_id) | Q(outlet_pengiriman_id=request.user.penempatan_toko_id))).exclude(log_pengiriman__status_pengiriman='done').order_by("-pk").distinct()
			elif hasattr(request.user, 'penempatan_gudang_id') and request.user.penempatan_gudang_id :
				# data_log = Pengiriman.objects.filter(log_pengiriman__status_pengiriman='done')
				data_log = Pengiriman.objects.filter(Q(is_active=True) & Q(log_pengiriman__id_kurir__penempatan_gudang_id=request.user.penempatan_gudang_id)).exclude(log_pengiriman__status_pengiriman='done').order_by("-pk").distinct()

		return render(request, 'mobile_kurir/templates/dashboard_detail/dashboard_detail.html', {
			'is_active_dashboard': 'active',
			'title': title,
			'link_nav': title if title else detail_dipilih,
			'data_log': data_log
		})