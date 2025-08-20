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
from django.db.models.functions import Lower, Concat

from .custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

def check_(username, email):
	try:
		print(data)
		if User.objects.filter(Q(username__icontains=username)|Q(email__icontains=username)).exists():
			return False
		else:
			return True
	except:
		return True

def check_data_update(username, email, id):
	try:
		if User.objects.exclude(id=id).filter(Q(username__iexact=username)|Q(email__iexact=email)).exists():
			return False
		else:
			return True
	except:
		return True

@method_decorator(login_required, name='get')
class PelangganView(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self,request):
		form = PelangganForm()
		pelanggans = User.objects.all()
		# if request.user.is_staff :
		datas = list(User.objects.values().filter(Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company')))
		# elif hasattr(request.user, 'penempatan_toko_id') :
		# 	total_pelanggan_telp = list(Pengiriman.objects.filter(outlet_pengiriman_id=request.user.penempatan_toko_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('no_telp_pengirim', flat=True))
		# 	total_pelanggan_nama = list(Pengiriman.objects.filter(outlet_pengiriman_id=request.user.penempatan_toko_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('nama_pengirim', flat=True))
		# 	datas = list(User.objects.values().filter(Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company'), no_telp__in=total_pelanggan_telp, first_name__in=total_pelanggan_nama))
		# elif hasattr(request.user, 'penempatan_gudang_id') :
		# 	total_pelanggan_telp = list(Pengiriman.objects.filter(gudang_pengiriman_id=request.user.penempatan_gudang_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('no_telp_pengirim', flat=True))
		# 	total_pelanggan_nama = list(Pengiriman.objects.filter(gudang_pengiriman_id=request.user.penempatan_gudang_id).values_list('nama_pengirim', 'no_telp_pengirim').distinct().values_list('nama_pengirim', flat=True))
		# 	datas = list(User.objects.values().filter(Q(register_sebagai__contains='personal') | Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company'), no_telp__in=total_pelanggan_telp, first_name__in=total_pelanggan_nama))

		data_list = []
		data_pelanggan = []
		i = 1
		for data in datas:
			data_list = [i]
			data_list.append(data['no_personil'])
			data_list.append(data['first_name'])
			data_list.append(data['no_telp'])

			if data['is_active']:
				status = ' <span class="badge badge-success">Active</span>'
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Arsipkan Pelanggan" data-id="' + str(data['id']) + '" data-nama="' + str(data['first_name']) + '"class="btn btn-warning btn-sm arsipPelanggan"><i class="fa fa-fw fa-archive"></i></a>'
			else:
				status = ' <span class="badge badge-danger">Tidak Aktif</span>'
				btn_arsip = '<a href="javascript:void(0)" data-toggle="tooltip" title="Kembalikan Pelanggan" data-id="' + str(data['id']) + '" data-nama="' + str(data['first_name']) + '"class="btn btn-info btn-sm unarsipPelanggan"><i class="fa fa-fw fa-upload"></i></a>'

			if data['register_sebagai'] == 'personal':
				data_list.append('<span class="badge badge-success">Personal</span>' + status)
			elif data['register_sebagai'] == 'goverment':
				data_list.append('<span class="badge badge-warning">Goverment</span>' + status)
			elif data['register_sebagai'] == 'company':
				data_list.append('<span class="badge badge-info">Company</span>' + status)
			else:
				data_list.append('<span class="badge badge-danger">Empty</span>' + status)
			
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Edit Pelanggan" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editPelanggan"><i class="fa fa-fw fa-edit"></i></a><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Pengguna" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailPelanggan"><i class="fa fa-fw fa-eye"></i></a>'+btn_arsip+'<a href="javascript:void(0)" data-toggle="tooltip" title="Delete Pelanggan" data-id="' + str(data['id']) + '" data-nama="' + str(data['first_name']) + '"class="btn btn-danger btn-sm deletePelanggan"><i class="fa fa-fw fa-trash-alt"></i></a></div></center>')
			i =  i+1
			data_pelanggan.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_pelanggan}, status=200)

		return render(request, 'pelanggan/index.html', context={'form': form, 'pelanggans': pelanggans})

	@csrf_exempt
	def post(self, request):
		if check_(username=request.POST.get('username'), email=request.POST.get('email')):
			form = PelangganForm(request.POST)
			form_pelanggan_detail = PelangganDetailInfoForm(request.POST)

			if form.is_valid():
				try:
					new_pelanggan = form.save(commit=False)
					password = new_pelanggan.password
					new_pelanggan.no_personil = generate_id('CR', 8)
					new_pelanggan.set_password(password)
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

					data = model_to_dict(new_pelanggan)
					data.pop('photo')
					return JsonResponse({'pelanggan': data, 'msg': 'Berhasil Menambah data Pelanggan', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Menambah data Pelanggan <br> {}'.format(e), 'type': 'error'}, status=422)
			else:
				error = [er[0] for er in form.errors.values()]
				error = "<br> ".join(error)
				return JsonResponse({'msg': 'Gagal Menambah Data, Form Input Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
		else:
			return JsonResponse({'msg': 'Username / Email Sudah Ada!', 'type': 'error'}, status=422)
		

class PelangganDetail(View):
	# @method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			pelanggan = User.objects.get(id = request.GET.get('id'))
			photo = pelanggan.photo.url if pelanggan.photo else ''
			try :
				detail_pelanggan = InformasiPelanggan.objects.filter(pelanggan_id=pelanggan.id).values('provinsi_id','provinsi__nama_provinsi', 'kota_id', 'kota_id', 'kota__nama_kota', 'kecamatan_id', 'kecamatan__nama_kecamatan', 'desa_id', 'desa__nama_desa', 'kode_pos_id', 'kode_pos__kode_pos').first()
			except Exception as e:
				print(e)
				detail_pelanggan = {}

			data = {
				'id': pelanggan.id,
				'no_personil': pelanggan.no_personil,
				'first_name': pelanggan.first_name,
				'no_telp': pelanggan.no_telp,
				'alamat': pelanggan.alamat,
				'email': pelanggan.email,
				'username': pelanggan.username,
				'register_sebagai' : pelanggan.register_sebagai,
				'detail_pelanggan': detail_pelanggan
			}
			
			return JsonResponse({'data': data, 'msg': 'Berhasil Mengambil Data pelanggan', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Pelanggan <br> {}'.format(e), 'type': 'error'})

	def post(self, request):
		try:
			if check_data_update(username=request.POST.get('username'), email=request.POST.get('email'), id=request.POST.get('id')): 
				obj = User.objects.get(id = request.POST.get('id'))
				obj.first_name = request.POST.get('first_name')
				obj.username = request.POST.get('username')
				obj.no_telp = request.POST.get('no_telp')
				obj.alamat = request.POST.get('alamat')
				obj.email = request.POST.get('email')
				obj.register_sebagai = request.POST.get('register_sebagai')

				if request.POST.get('password'):
					if request.POST.get('password') == request.POST.get('re_password'):
						obj.set_password(request.POST.get('password'))
					else:
						return JsonResponse({'msg': 'Password Tidak Sama!', 'type': 'error'}, status=422)

				try:
					obj.save()
					try :
						pelangganDetail, created = InformasiPelanggan.objects.get_or_create(pelanggan_id=obj,
							defaults={
								'provinsi_id': request.POST.get('provinsi'),
								'kota_id': request.POST.get('kota'),
								'kecamatan_id': request.POST.get('kecamatan'),
								'desa_id': request.POST.get('desa'),
								'kode_pos_id': request.POST.get('kode_pos')
							}
						)
						if not created :
							pelangganDetail.provinsi_id = request.POST.get('provinsi')
							pelangganDetail.kota_id = request.POST.get('kota')
							pelangganDetail.kecamatan_id = request.POST.get('kecamatan')
							pelangganDetail.desa_id = request.POST.get('desa')
							pelangganDetail.kode_pos_id = request.POST.get('kode_pos')
							pelangganDetail.save()
					except Exception as e:
						print("EKSSEPSI", e)
						pass

					return JsonResponse({'msg': 'Berhasil Update data Pelanggan', 'type': 'success'})
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Update data Pelanggan <br> {}'.format(e), 'type': 'error'})
			else:
				return JsonResponse({'msg': 'Username / Email Sudah Ada!', 'type': 'error'}, status=422)

		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil data dari database!, <br> {}'.format(e), 'type': 'error'}, status=400)

class PelangganDelete(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def post(self, request):
		pelanggan = User.objects.get(id=request.POST.get('id'))
		try:
			pelanggan.delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data Pelanggan', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengapus Data Pelanggan <br>{}'.format(e), 'type': 'error'}, status=443)

class PelangganArsip(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def post(self, request):
		pelanggan = User.objects.get(id=request.POST.get('id'))
		try:
			pelanggan.is_active = False
			pelanggan.save()
			return JsonResponse({'msg': 'Berhasil Mengarsipkan Pelanggan', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengarsipkan Pelanggan <br>{}'.format(e), 'type': 'error'}, status=443)

class PelangganUnarsip(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def post(self, request):
		pelanggan = User.objects.get(id=request.POST.get('id'))
		try:
			pelanggan.is_active = True
			pelanggan.save()
			return JsonResponse({'msg': 'Berhasil Mengaktifkan Pelanggan', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengaktifkan Pelanggan <br>{}'.format(e), 'type': 'error'}, status=443)

class PelangganCari(View):
	def get(self, request):
		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET['page'])
			total_counts = User.objects.filter(Q(is_active=True) & (Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company') | Q(register_sebagai__contains='personal')) & (Q(first_name__icontains=q) | Q(alamat__icontains=q))).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(User.objects.values().filter(Q(is_active=True) & (Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company') | Q(register_sebagai__contains='personal')) & (Q(first_name__icontains=q) | Q(alamat__icontains=q) | Q(register_sebagai__icontains=q)))[start_p:pages])
			
		else:
			page = int(request.GET['page'])
			total_counts = User.objects.filter(Q(is_active=True) & (Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company') | Q(register_sebagai__contains='personal'))).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(User.objects.values().filter(Q(is_active=True) & (Q(register_sebagai__contains='goverment') | Q(register_sebagai__contains='company') | Q(register_sebagai__contains='personal')))[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:
			if data['register_sebagai'] == 'goverment':
				badge = data['first_name'] + ', ' + data['alamat'] + ' <span class="badge badge-warning">'+ data['register_sebagai'] +'</span>'
			elif data['register_sebagai'] == 'company':
				badge = data['first_name'] + ', ' + data['alamat'] + ' <span class="badge badge-info">'+ data['register_sebagai'] +'</span>'
			else:
				badge = data['first_name'] + ', ' + data['alamat'] + ' <span class="badge badge-success">'+ data['register_sebagai'] +'</span>'

			data_list.append({'id': data['id'], 'text': (data['first_name'] + " , " + data['alamat']), 'html': badge })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)