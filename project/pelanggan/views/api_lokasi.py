from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime
from random import randint

from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from ekspedisi.models import Provinsi, Kota, Kecamatan, Desa, KodePos

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.db.models import Q

class APIProvinsi(View):
	def get(self, request):
		total_counts = 0
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Provinsi.objects.filter(Q(is_active=True) & Q(nama_provinsi__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Provinsi.objects.values().filter(Q(is_active=True) & Q(nama_provinsi__icontains=q)).order_by('nama_provinsi')[start_p:pages])
			
		else:
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Provinsi.objects.filter(is_active = True).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Provinsi.objects.values().filter(is_active = True).order_by('nama_provinsi')[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['nama_provinsi'] })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)



class APIKota(View):
	def get(self, request, provinsi_id):
		total_counts = 0
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Kota.objects.filter(Q(is_active=True) & Q(provinsi_id = provinsi_id) & Q(nama_kota__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Kota.objects.values().filter(Q(is_active=True) & Q(provinsi_id = provinsi_id) & Q(nama_kota__icontains=q)).order_by('nama_kota')[start_p:pages])
			
		else:
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Kota.objects.filter(is_active = True, provinsi_id = provinsi_id).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Kota.objects.values().filter(is_active = True, provinsi_id = provinsi_id).order_by('nama_kota')[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['nama_kota'] })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)


class APIKecamatan(View):
	def get(self, request, kota_id):
		total_counts = 0
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Kecamatan.objects.filter(Q(is_active=True) & Q(kota_id = kota_id) & Q(nama_kecamatan__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Kecamatan.objects.values().filter(Q(is_active=True) & Q(kota_id = kota_id) & Q(nama_kecamatan__icontains=q)).order_by('nama_kecamatan')[start_p:pages])
			
		else:
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Kecamatan.objects.filter(is_active = True, kota_id = kota_id).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Kecamatan.objects.values().filter(is_active = True, kota_id = kota_id).order_by('nama_kecamatan')[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['nama_kecamatan'] })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)


class APIDesa(View):
	def get(self, request, kecamatan_id):
		total_counts = 0
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Desa.objects.filter(Q(is_active=True) & Q(kecamatan_id = kecamatan_id) & Q(nama_desa__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Desa.objects.values().filter(Q(is_active=True) & Q(kecamatan_id = kecamatan_id) & Q(nama_desa__icontains=q)).order_by('nama_desa')[start_p:pages])
			
		else:
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = Desa.objects.filter(is_active = True, kecamatan_id = kecamatan_id).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Desa.objects.values().filter(is_active = True, kecamatan_id = kecamatan_id).order_by('nama_desa')[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['nama_desa'] })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)

class APIKodePos(View):
	def get(self, request, provinsi_id, kota_id, kecamatan_id, desa_id):
		total_counts = 0
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = KodePos.objects.filter(Q(is_active=True) & Q(provinsi_id = kecamatan_id) & Q(kota_id = kota_id) & Q(kecamatan_id = kecamatan_id) & Q(desa_id = desa_id) & Q(kode_pos__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(KodePos.objects.values().filter(Q(is_active=True) & Q(provinsi_id = kecamatan_id) & Q(kota_id = kota_id) & Q(kecamatan_id = kecamatan_id) & Q(desa_id = desa_id) & Q(kode_pos__icontains=q))[start_p:pages])
			
		else:
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = KodePos.objects.filter(is_active = True, provinsi_id = provinsi_id, kota_id = kota_id, kecamatan_id = kecamatan_id, desa_id = desa_id).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(KodePos.objects.values().filter(is_active = True, provinsi_id = provinsi_id, kota_id = kota_id, kecamatan_id = kecamatan_id, desa_id = desa_id)[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['kode_pos'] })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)

class APIKodePos2(View):
	def get(self, request, provinsi_id, kota_id, kecamatan_id):
		total_counts = 0
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = KodePos.objects.filter(Q(is_active=True) & Q(provinsi_id = kecamatan_id) & Q(kota_id = kota_id) & Q(kecamatan_id = kecamatan_id) & Q(kode_pos__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(KodePos.objects.values().filter(Q(is_active=True) & Q(provinsi_id = kecamatan_id) & Q(kota_id = kota_id) & Q(kecamatan_id = kecamatan_id) & Q(kode_pos__icontains=q))[start_p:pages])
			
		else:
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = KodePos.objects.filter(is_active = True, provinsi_id = provinsi_id, kota_id = kota_id, kecamatan_id = kecamatan_id).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(KodePos.objects.values().filter(is_active = True, provinsi_id = provinsi_id, kota_id = kota_id, kecamatan_id = kecamatan_id)[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['kode_pos'] })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)