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

from .custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class AdminOutletOrderView(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			outlet_tugas = request.user.penempatan_toko.id
		except:
			outlet_tugas = 0
		form = OrderPickupForm()
		datas = list(OrderPickup.objects.filter(is_active = True, id_toko = outlet_tugas).order_by('-created_at').select_related('user', 'toko').values())
		data_list = []
		data_order = []
		i = 1
		for data in datas:
			data_list = [i]
			pelanggan = model_to_dict(User.objects.exclude(role__in=['adm_gudang', 'adm_outlet', 'kurir']).filter(id= data['id_customer_id']).first())
			data_list.append(data['id_order'])
			data_list.append(pelanggan['first_name'])
			# data_list.append(pelanggan['alamat'])
			if data['alamat_pengirim_alt'] :
				data_list.append(data['alamat_pengirim_alt'])
			else :
				data_list.append(pelanggan['alamat'])

			data_list.append(data['status'])
			data_list.append('<center><a href="javascript:void(0)" data-toggle="tooltip" title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-warning btn-sm downloadBilling"><i class="fa fa-fw fa-file-alt"></i></a></center>')
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Order" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrderPickup"><i class="fa fa-fw fa-eye"></i> Detail</a></div></center>')
			i =  i+1
			data_order.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_order}, status=200)

		return render(request, 'order_pickup_outlet/index.html', context={'form': form})

class AdminOutletOrderHistoryView(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			outlet_tugas = request.user.penempatan_toko.id
		except:
			outlet_tugas = 0
		form = OrderPickupForm()
		datas = list(OrderPickup.objects.filter(is_active = False, id_toko = outlet_tugas).select_related('user', 'toko').values())
		data_list = []
		data_order = []
		i = 1
		for data in datas:
			data_list = [i]
			pelanggan = model_to_dict(User.objects.exclude(role__in=['adm_gudang', 'adm_outlet', 'kurir']).filter(id= data['id_customer_id']).first())
			data_list.append(data['id_order'])
			if data['status']=='cancel':
				data_list.append('<span class="badge badge-danger">'+data['status']+'</span><br>')
			else:
				data_list.append('<span class="badge badge-success">'+data['status']+'</span><br>')
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Download Label" data-id="' + str(data['id']) + '" class="btn btn-warning btn-sm downloadBilling"><i class="fa fa-fw fa-file-alt"></i></a><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Order" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrderPickup"><i class="fa fa-fw fa-eye"></i></a></div></center>')
			i =  i+1
			data_order.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_order}, status=200)

		return render(request, 'order_pickup_outlet/index.html', context={'form': form})

class AdminOutletOrderDetail(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request):
		try:
			order = get_object_or_404(OrderPickup, id = request.GET.get('id'))
			formatedDate = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
			data_pickup = model_to_dict(get_object_or_404(OrderPickup, id = request.GET.get('id')))

			try :
				kurirPickup = User.objects.get(id=data_pickup['kurir_id'])
				data_pickup['kurir_nama'] = str(kurirPickup.first_name) +" || "+ str(kurirPickup.username)
			except :
				try :
					data_pickup['kurir_nama'] = 'Pilih Kurir'
				except :
					pass

			try :
				layanan = Layanan.objects.get(id=data_pickup['jenis_pengiriman'])
				data_pickup['jenis_pengiriman'] = layanan.nama_layanan.capitalize()
			except :
				try :
					data_pickup['jenis_pengiriman'] = 'Tidak diketahui'
				except :
					pass

			try :
				jenis_barang = JenisKiriman.objects.get(id=int(data_pickup['jenis_barang']))
				data_pickup['jenis_barang'] = jenis_barang.nama.capitalize()
			except Exception as e:
				try :
					jenis_barang = JenisKiriman.objects.get(nama__iexact=data_pickup['jenis_barang'])
					data_pickup['jenis_barang'] = jenis_barang.nama.capitalize()
				except :
					pass

			data_pelanggan = model_to_dict(User.objects.exclude(role__in=['adm_gudang', 'adm_outlet', 'kurir']).filter(id= data_pickup['id_customer']).first())
			if order.alamat_pengirim_alt :
				data_pelanggan['alamat'] = order.alamat_pengirim_alt

			try :
				data_pelanggan.pop('photo')
				data_pelanggan.pop('role')
				data_pelanggan.pop('is_staff')
				data_pelanggan.pop('penempatan_toko')
				data_pelanggan.pop('penempatan_gudang')
			except:
				pass
			data_toko = model_to_dict(get_object_or_404(Toko, id = data_pickup['id_toko']))
			try:
				data_pengemasan = model_to_dict(get_object_or_404(Pengemasan, id = data_pickup['id_pengemasan']))
			except:
				data_pengemasan = {
					'id': '',
					'id_pengemasan': '',
					'nama_pengemasan': 'Tidak Menggunakan Pengemasan',
					'bahan_pengemasan': '',
					'tarif': '',
					'is_active': ''
				}

			return JsonResponse({'order_pickup': data_pickup, 'pelanggan': data_pelanggan, 'toko': data_toko, 'pengemasan': data_pengemasan, 'tgl_order': formatedDate, 'msg': 'Berhasil Mengambil Data Order Pickup', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Order Pickup, {}'.format(e), 'type': 'error'}, status=422)

	def post(self, request):
		try:
			obj=OrderPickup.objects.filter(id=request.POST.get('id'))
			status_order = request.POST.get('status')
			kurir_pickup = request.POST.get('kurir_id')
			obj.update(status=status_order, scan_by=request.user, kurir_id_id=kurir_pickup)
			return JsonResponse({'msg': 'Berhasil Update Order Pickup', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Update Order Pickup', 'type': 'error' }, status=422)