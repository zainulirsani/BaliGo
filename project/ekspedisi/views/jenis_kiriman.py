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
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils import timezone


def check_(data):
	try:
		if JenisKiriman.objects.filter(Q(nama__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_data_update(data, id):
	try:
		if JenisKiriman.objects.filter(Q(nama__iexact=data)).exists():
			return False
		else:
			return True
	except:
		return True

class JenisKirimanView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = JenisKirimanForm()
		jenis_kiriman = list(JenisKiriman.objects.all().values())
		data_list = []
		data_jenis_kiriman = []
		i = 1
		for data in jenis_kiriman:
			data_list = [i]
			data_list.append(data['nama'])

			if data['is_active'] == True:
				data_list.append('<span class="badge bg-success">AKTIF</span>')
				tombol_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Arsipkan Jenis Kiriman" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama']) + '"class="btn btn-warning btn-sm arsipJenisKiriman"><i class="fa fa-fw fa-archive"></i></a>'
			else:
				data_list.append('<span class="badge bg-warning">ARSIP</span>')
				tombol_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Restore Jenis Kiriman" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama']) + '"class="btn btn-success btn-sm unarsipJenisKiriman"><i class="fa fa-fw fa-upload"></i></a>'
			data_list.append(timezone.localtime(data['updated_at']).strftime('%Y-%m-%d %H:%M:%S'))

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Edit Jenis Kiriman" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editJenisKiriman"><i class="fa fa-fw fa-edit"></i></a>'+tombol_arsip+'<a href="javascript:void(0)" data-toggle="tooltip" title="Delete Jenis Kiriman" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama']) + '"class="btn btn-danger btn-sm deleteJenisKiriman"><i class="fa fa-fw fa-trash-alt"></i></a></div></center>')
			i =  i+1
			data_jenis_kiriman.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_jenis_kiriman}, status=200)

		return render(request, 'jenis_kiriman/index.html', context={'form': form, 'jenis_kiriman': data_jenis_kiriman})

	@csrf_exempt
	def post(self, request):
		try : 
			form = JenisKirimanForm(request.POST)
			if check_(data = request.POST.get("nama")):
				if form.is_valid():
					try:
						tz = get_current_timezone()
						new_jenis_kiriman = form.save()
						return JsonResponse({'msg': 'Berhasil Menambah data jenis kiriman', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data jenis kiriman {}'.format(e), 'type': 'error'}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form jenis kiriman Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Nama jenis kiriman sudah ada!', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class JenisKirimanArsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			jenis_kiriman = JenisKiriman.objects.get(id=request.POST.get('id'))
			jenis_kiriman.is_active = False
			jenis_kiriman.save()
			return JsonResponse({'msg': 'Berhasil mengarsip data jenis kiriman', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal mengarsip data jenis kiriman', 'type': 'error'}, status=443)

class JenisKirimanUnarsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			jenis_kiriman = JenisKiriman.objects.get(id=request.POST.get('id'))
			jenis_kiriman.is_active = True
			jenis_kiriman.save()
			return JsonResponse({'msg': 'Berhasil mengembalikan data jenis kiriman', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal mengembalikan data jenis kiriman', 'type': 'error'}, status=443)

class JenisKirimanDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			jenis_kiriman = JenisKiriman.objects.get(id=request.POST.get('id')).delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data jenis kiriman', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data jenis kiriman', 'type': 'error'}, status=443)

class JenisKirimanDetail(View):
	# @method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			jenis_kiriman = get_object_or_404(JenisKiriman, id = request.GET.get('id'))
			
			return JsonResponse({'data': model_to_dict(jenis_kiriman), 'msg': 'Berhasil Mengambil Data jenis kiriman', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data jenis kiriman {}'.format(e), 'type': 'error'})

	def post(self, request):
		try: 
			obj = get_object_or_404(JenisKiriman, id = request.POST.get('id'))
			form = JenisKirimanForm(request.POST or None, instance = obj)
			if check_data_update(data = request.POST.get("nama"), id= request.POST.get('id')):
				if form.is_valid():
					try:
						tz = get_current_timezone()
						form.save()
						return JsonResponse({'msg': 'Berhasil Update data jenis kiriman', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Update data jenis kiriman {}'.format(e), 'type': 'error'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data jenis kiriman Form Tidak Valid', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Nama jenis kiriman Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})


class JenisKirimanToSelect2(View):
	@csrf_exempt
	def get(self, request):
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = JenisKiriman.objects.filter(Q(is_active=True) & Q(nama__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(JenisKiriman.objects.values().filter(Q(is_active=True) & Q(nama__icontains=q))[start_p:pages])
			
		else:
			page = int(request.GET.get('page') if request.GET.get('page') else 1)
			total_counts = JenisKiriman.objects.filter(is_active = True).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(JenisKiriman.objects.values().filter(is_active = True)[start_p:pages])
			

		data_list = []
		i = 1 
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['nama']})
		print(data_list)
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)