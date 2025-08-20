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
from django.utils import timezone

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

def check_(data):
	try:
		if Satuan.objects.filter(Q(nama_satuan__icontains=data)).exists():
			return False
		else:
			return True
	except:
		return True

def check_data_update(data, id):
	try:
		if Satuan.objects.filter(Q(nama_satuan__iexact=data)).exists():
			return False
		else:
			return True
	except:
		return True


class SatuanView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = SatuanForm()
		satuan = list(Satuan.objects.all().values())
		data_list = []
		data_satuan = []
		i = 1
		for data in satuan:
			data_list = [i]
			data_list.append(data['nama_satuan'])

			if data['is_active'] == True:
				data_list.append('<span class="badge bg-success">AKTIF</span>')
				tombol_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Arsipkan satuan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_satuan']) + '"class="btn btn-warning btn-sm arsipSatuan"><i class="fa fa-fw fa-archive"></i></a>'
			else:
				data_list.append('<span class="badge bg-warning">ARSIP</span>')
				tombol_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Restore satuan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_satuan']) + '"class="btn btn-success btn-sm unarsipSatuan"><i class="fa fa-fw fa-upload"></i></a>'

			data_list.append(timezone.localtime(data['updated_at']).strftime('%Y-%m-%d %H:%M:%S'))

			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Edit satuan" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editSatuan"><i class="fa fa-fw fa-edit"></i></a>'+tombol_arsip+'<a href="javascript:void(0)" data-toggle="tooltip" title="Delete satuan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama_satuan']) + '"class="btn btn-danger btn-sm deleteSatuan"><i class="fa fa-fw fa-trash-alt"></i></a></div></center>')
			i =  i+1
			data_satuan.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_satuan}, status=200)

		return render(request, 'satuan/index.html', context={'form': form, 'satuan': data_satuan})

	@csrf_exempt
	def post(self, request):
		try : 
			form = SatuanForm(request.POST)
			if check_(data = request.POST.get("nama_satuan")):
				if form.is_valid():
					try:
						new_satuan = form.save()
						return JsonResponse({'msg': 'Berhasil Menambah data satuan', 'type': 'success'}, status=200)
					except Exception as e :
						return JsonResponse({'msg': 'Gagal Menambah data satuan {}'.format(e), 'type': 'error'}, status=400)
				else:
					error = [er[0] for er in form.errors.values()]
					error = "<br> ".join(error)
					return JsonResponse({'msg': 'Gagal, Form satuan Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
			else:
				return JsonResponse({'msg': 'Nama satuan sudah ada!', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class SatuanArsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			satuan = Satuan.objects.get(id=request.POST.get('id'))
			satuan.is_active = False
			satuan.save()
			return JsonResponse({'msg': 'Berhasil mengarsip data satuan (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal mengarsip data satuan (Arsip)', 'type': 'error'}, status=443)

class SatuanUnarsip(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			satuan = Satuan.objects.get(id=request.POST.get('id'))
			satuan.is_active = True
			satuan.save()
			return JsonResponse({'msg': 'Berhasil mengembalikan data satuan', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal mengembalikan data satuan', 'type': 'error'}, status=443)


class SatuanDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request):
		try:
			satuan = Satuan.objects.get(id=request.POST.get('id')).delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data satuan', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data satuan', 'type': 'error'}, status=443)

class SatuanDetail(View):
	# @method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			satuan = get_object_or_404(Satuan, id = request.GET.get('id'))
			
			return JsonResponse({'data': model_to_dict(satuan), 'msg': 'Berhasil Mengambil Data satuan', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data satuan {}'.format(e), 'type': 'error'})

	def post(self, request):
		try: 
			obj = get_object_or_404(Satuan, id = request.POST.get('id'))
			form = SatuanForm(request.POST or None, instance = obj)
			if check_data_update(data = request.POST.get("nama_satuan"), id=request.POST.get('id')):
				if form.is_valid():
					try:
						form.save()
						return JsonResponse({'msg': 'Berhasil Update data satuan', 'type': 'success'}, status=200)
					except Exception as e:
						return JsonResponse({'msg': 'Gagal Update data satuan {}'.format(e), 'type': 'error'}, status=200)
				else:
					return JsonResponse({'msg': 'Gagal Update data satuan Form Tidak Valid', 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Nama satuan Sudah Ada!', 'type': 'error'}, status=422)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})


class SatuanToSelect2(View):
	def get(self, request):

		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET['page'])
			total_counts = Satuan.objects.filter(Q(is_active=True) & Q(nama_satuan__icontains=q)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Satuan.objects.values().filter(Q(is_active=True) & Q(nama_satuan__icontains=q))[start_p:pages])
			
		else:
			page = int(request.GET['page'])
			total_counts = Satuan.objects.filter(is_active = True).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Satuan.objects.values().filter(is_active = True)[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': data['nama_satuan']})
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)