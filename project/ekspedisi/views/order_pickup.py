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
from django.db.models import Q, F
from django.utils.timezone import get_current_timezone, make_aware, now

from .custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class OrderPickupPilihOutletGudangManual(View) :
	@csrf_exempt
	def post(self, request):
		if request.is_ajax() :
			try : 
				outlet_pengirim = {}
				outlet_penerima = {}
				gudang_pengirim = {}
				gudang_penerima = {}

				kec_pengirim = request.POST.get('kecamatan_pengirim', False)
				kec_penerima = request.POST.get('kecamatan_penerima', False)
				if kec_pengirim and kec_penerima:
					outlet_pengirim = list(Toko.objects.filter(is_active=True, kecamatan_toko_id=kec_pengirim).values('id', 'nama_toko','alamat',kode_pos=F('kode_pos_toko__kode_pos'),desa=F('desa_toko__nama_desa'),kec=F('kecamatan_toko__nama_kecamatan'),kota=F('kota_toko__nama_kota'),provinsi=F('provinsi_toko__nama_provinsi'))) if Toko.objects.filter(is_active=True, kecamatan_toko_id=kec_pengirim).values('id', 'nama_toko') else {}

					gudang_pengirim = list(Gudang.objects.filter(is_active=True, kecamatan_gudang_id=kec_pengirim).values('id', 'nama_gudang','alamat',kode_pos=F('kode_pos_gudang__kode_pos'),desa=F('desa_gudang__nama_desa'),kec=F('kecamatan_gudang__nama_kecamatan'),kota=F('kota_gudang__nama_kota'),provinsi=F('provinsi_gudang__nama_provinsi'))) if Gudang.objects.filter(is_active=True, kecamatan_gudang_id=kec_pengirim).values('id', 'nama_gudang') else {}

					outlet_penerima = list(Toko.objects.filter(is_active=True, kecamatan_toko_id=kec_penerima).values('id', 'nama_toko','alamat',kode_pos=F('kode_pos_toko__kode_pos'),desa=F('desa_toko__nama_desa'),kec=F('kecamatan_toko__nama_kecamatan'),kota=F('kota_toko__nama_kota'),provinsi=F('provinsi_toko__nama_provinsi'))) if Toko.objects.filter(is_active=True, kecamatan_toko_id=kec_penerima).values('id', 'nama_toko') else {}

					gudang_penerima = list(Gudang.objects.filter(is_active=True, kecamatan_gudang_id=kec_penerima).values('id', 'nama_gudang','alamat',kode_pos=F('kode_pos_gudang__kode_pos'),desa=F('desa_gudang__nama_desa'),kec=F('kecamatan_gudang__nama_kecamatan'),kota=F('kota_gudang__nama_kota'),provinsi=F('provinsi_gudang__nama_provinsi'))) if Gudang.objects.filter(is_active=True, kecamatan_gudang_id=kec_penerima).values('id', 'nama_gudang') else {}

					# print(gudang_pengirim, gudang_penerima)
					return JsonResponse({'type':'success', 'data':{'outlet_pengirim':outlet_pengirim, 'outlet_penerima':outlet_penerima, 'gudang_pengirim':gudang_pengirim, 'gudang_penerima':gudang_penerima}}, status=200)
				else :
					return JsonResponse({'type':'error', 'msg': 'Tidak dapat membaca Outlet Pengirim serta Kecamatan pengirim dan penerima'}, status=400)

			except Exception as e :
				return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)
		else :
			return JsonResponse({'msg': 'Permintaan tidak dapat diteruskan karena tidak sesuai'.format(e), 'type': 'error'}, status=412)

class OrderPickupView(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request):
		
		return render(request, 'order_pickup/index.html')

	@csrf_exempt
	def post(self, request):
		form = OrderPickupForm(request.POST)
		if form.is_valid():
			try:
				tz = get_current_timezone()
				new_order = form.save(commit=False)
				new_order.id_order = generate_id('OP', 8)
				new_order.save()

				return JsonResponse({'gudang': model_to_dict(new_order), 'msg': 'Berhasil Menambah data Order Pick Up', 'type': 'success'}, status=200)
			except:
				return JsonResponse({'msg': 'Gagal Menambah data Order Pick Up', 'type': 'error'}, status=200)
		else:
			return JsonResponse({'msg': 'Mohon di cek kembali semua kelengkapan dan format data pada setiap kolom', 'type': 'error'}, status=422)

class OrderPickupDetail(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			data_pickup = model_to_dict(get_object_or_404(OrderPickup, id = id))
			data_pelanggan = model_to_dict(User.objects.exclude(role__in=['adm_gudang', 'adm_outlet', 'kurir']).filter(id=data_pickup['id_customer']).first())
			try:
				data_toko = model_to_dict(get_object_or_404(Toko, id = data_pickup['id_toko']))
			except:
				data_toko = 'kosong'
			try:
				data_gudang = model_to_dict(get_object_or_404(Gudang, id = data_pickup['id_gudang']))
			except:
				data_gudang = 'kosong'

			return JsonResponse({'order_pickup': data_pickup, 'pelanggan': data_pelanggan, 'toko': data_toko, 'gudang': data_gudang, 'msg': 'Berhasil Mengambil Data Order Pickup', 'type': 'success'})
		except:
			return JsonResponse({'msg': 'Gagal Mengambil Data Order Pickup', 'type': 'error'})

class OrderPickupOutlet(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request):
		datas = list(Toko.objects.values().filter(is_active = True))
		data_list = []
		data_toko = []
		i = 1
		for data in datas:
			data_list = [i]
			data_list.append(data['id_toko'])
			data_list.append(data['nama_toko'])
			data_list.append(data['alamat'])
			data_list.append('<center><div class="btn-group" role="group"><a href="list_outlet/' + str(data['id']) + '/detail/" data-original-title="Lihat List Order" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm listOrderAtOutlet"><i class="fa fa-fw fa-eye"></i> <span class="detail_text">Lihat List Order</span></a></div></center>')
			i =  i+1
			data_toko.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_toko}, status=200)

		return JsonResponse({'data': data_toko}, status=200)

class OrderPickupOutletList(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request, id):
		url_order = 'order_pickup/list_outlet/' + str(id) + '/detail/'
		form = OrderPickupForm()
		orders = OrderPickup.objects.all()
		datas = list(OrderPickup.objects.filter(is_active = True, id_toko = id).select_related('user', 'toko').values())
		data_list = []
		data_order = []
		i = 1
		for data in datas:
			data_list = [i]
			pelanggan = model_to_dict(User.objects.exclude(role__in=['adm_gudang', 'adm_outlet', 'kurir']).filter(id= data['id_customer_id']).first())
			data_list.append(data['id_order'])
			data_list.append(pelanggan['first_name'])
			if data['alamat_pengirim_alt'] :
				data_list.append(data['alamat_pengirim_alt'])
			else :
				data_list.append(pelanggan['alamat'])
			status_data = ''
			if data['status'] == 'done':
				status_data = '<span class="badge badge-success">Done</span><br>'
			elif data['status'] == 'cancel':
				status_data = '<span class="badge badge-danger">Cancel</span><br>'
			else:
				status_data = '<span class="badge badge-info">'+data['status']+'</span><br>'
			data_list.append(status_data)
			data_list.append('<center><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-warning btn-sm downloadBilling"><i class="fa fa-fw fa-file-alt"></i></a></center>')
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Detail Order" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrderPickup"><i class="fa fa-fw fa-eye"></i> Detail</a></div></center>')
			i =  i+1
			data_order.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_order}, status=200)

		return render(request, 'order_pickup/order_at_outlet.html', context={'form': form, 'url_order': url_order})

class OrderPickupOutletHistoryList(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request, id):
		form = OrderPickupForm()
		orders = OrderPickup.objects.all()
		datas = list(OrderPickup.objects.filter(is_active = False, id_toko = id).select_related('user', 'toko').values())
		data_list = []
		data_order = []
		i = 1
		for data in datas:
			data_list = [i]
			pelanggan = model_to_dict(User.objects.exclude(role__in=['adm_gudang', 'adm_outlet', 'kurir']).filter(id= data['id_customer_id']).first())
			data_list.append(data['id_order'])
			data_list.append(pelanggan['first_name'])
			if data['alamat_pengirim_alt'] :
				data_list.append(data['alamat_pengirim_alt'])
			else :
				data_list.append(pelanggan['alamat'])
			status_data = ''
			if data['status'] == 'done':
				status_data = '<span class="badge badge-success">Done</span><br>'
			elif data['status'] == 'cancel':
				status_data = '<span class="badge badge-danger">Cancel</span><br>'
			else:
				status_data = '<span class="badge badge-info">'+data['status']+'</span><br>'
			data_list.append(status_data)
			data_list.append('<center><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-warning btn-sm downloadBilling"><i class="fa fa-fw fa-file-alt"></i></a></center>')
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Detail Order" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrderPickup"><i class="fa fa-fw fa-eye"></i> Detail</a></div></center>')
			i =  i+1
			data_order.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_order}, status=200)

class OrderPickupOutletDetail(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			order = get_object_or_404(OrderPickup, id = id)
			print(order);
			formatedDate = order.created_at
			data_pickup = model_to_dict(get_object_or_404(OrderPickup, id = id))
			try :
				kurirPickup = User.objects.get(id=data_pickup['kurir_id'])
				data_pickup['kurir_nama'] = str(kurirPickup.first_name) +" || "+ str(kurirPickup.username)
			except :
				try :
					data_pickup['kurir_nama'] = 'Nama tidak diketahui, Silahkan update kembali'
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
					try :
						data_pickup['jenis_barang'] = 'Tidak diketahui'
					except :
						pass
			try :
				provinsi_pengirim = Provinsi.objects.get(id=data_pickup['provinsi_pengirim'])
				provinsi_penerima = Provinsi.objects.get(id=data_pickup['provinsi_penerima'])
				data_pickup['provinsi_penerima_nama'] = provinsi_penerima.nama_provinsi
				data_pickup['provinsi_pengirim_nama'] = provinsi_pengirim.nama_provinsi

				kecamatan_pengirim = Kecamatan.objects.get(id=data_pickup['kecamatan_pengirim'])
				kecamatan_penerima = Kecamatan.objects.get(id=data_pickup['kecamatan_penerima'])
				data_pickup['kecamatan_penerima_nama'] = kecamatan_penerima.nama_kecamatan
				data_pickup['kecamatan_pengirim_nama'] = kecamatan_pengirim.nama_kecamatan

				kota_pengirim = Kota.objects.get(id=data_pickup['kota_pengirim'])
				kota_penerima = Kota.objects.get(id=data_pickup['kota_penerima'])
				data_pickup['kota_penerima_nama'] = kota_penerima.nama_kota
				data_pickup['kota_pengirim_nama'] = kota_pengirim.nama_kota

				desa_pengirim = Desa.objects.get(id=data_pickup['desa_pengirim'])
				desa_penerima = Desa.objects.get(id=data_pickup['desa_penerima'])
				data_pickup['desa_penerima_nama'] = desa_penerima.nama_desa
				data_pickup['desa_pengirim_nama'] = desa_pengirim.nama_desa

				kodepos_pengirim = KodePos.objects.get(id=data_pickup['kode_pos_pengirim'])
				kodepos_penerima = KodePos.objects.get(id=data_pickup['kode_pos_penerima'])
				data_pickup['kode_pos_penerima_nama'] = kodepos_penerima.kode_pos
				data_pickup['kode_pos_pengirim_nama'] = kodepos_pengirim.kode_pos

			except Exception as e:
				print(e)
				data_pickup['provinsi_penerima_nama'] = ''
				data_pickup['provinsi_pengirim_nama'] = ''
				data_pickup['kecamatan_penerima_nama'] = ''
				data_pickup['kecamatan_pengirim_nama'] = ''
				data_pickup['kota_penerima_nama'] = ''
				data_pickup['kota_pengirim_nama'] = ''
				data_pickup['kode_pos_penerima_nama'] = ''
				data_pickup['kode_pos_pengirim_nama'] = ''

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
			return JsonResponse({'msg': 'Gagal Mengambil Data Order Pickup, {}'.format(e), 'type': 'error'})

	def post(self, request, id):

		try:
			obj=OrderPickup.objects.filter(id=id)
			status_order = request.POST.get('status')
			obj.update(status=status_order)
			return JsonResponse({'msg': 'Berhasil Update Order Pickup', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Update Order Pickup', 'type': 'error' })



class OrderPickupGudang(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request):
		datas = list(Gudang.objects.values().filter(is_active = True))
		data_list = []
		data_gudang = []
		i = 1
		for data in datas:
			data_list = [i]
			data_list.append(data['id_gudang'])
			data_list.append(data['nama_gudang'])
			data_list.append(data['alamat'])
			data_list.append('<center><div class="btn-group" role="group"><a href="list_gudang/' + str(data['id']) + '/detail/" data-toggle="tooltip" data-original-title="Lihat List Order" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm listOrderAtOutlet"><i class="fa fa-fw fa-eye"></i> <span class="detail_text">Lihat List Order</span></a></div></center>')
			i =  i+1
			data_gudang.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_gudang}, status=200)

		return JsonResponse({'data': data_gudang}, status=200)


class OrderPickupGudangList(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request, id):
		url_order = 'order_pickup/list_gudang/' + str(id) + '/detail/'
		form = OrderPickupForm()
		orders = OrderPickup.objects.all()
		datas = list(OrderPickup.objects.filter(is_active = True, id_gudang = id).select_related('user', 'gudang').values())
		data_list = []
		data_order = []
		i = 1
		for data in datas:
			data_list = [i]
			pelanggan = model_to_dict(User.objects.exclude(role__in=['adm_gudang', 'adm_outlet', 'kurir']).filter(id= data['id_customer_id']).first())
			data_list.append(data['id_order'])
			data_list.append(pelanggan['first_name'])
			if data['alamat_pengirim_alt'] :
				data_list.append(data['alamat_pengirim_alt'])
			else :
				data_list.append(pelanggan['alamat'])
			data_list.append(data['status'])
			data_list.append('<center><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-warning btn-sm downloadBilling"><i class="fa fa-fw fa-file-alt"></i></a></center>')
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Detail Order" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrderPickup"><i class="fa fa-fw fa-eye"></i> Detail</a></div></center>')
			i =  i+1
			data_order.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_order}, status=200)

		return render(request, 'order_pickup/order_at_gudang.html', context={'form': form, 'url_order': url_order})

class OrderPickupGudangDetail(View):
	@method_decorator(admin_outlet_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			order = get_object_or_404(OrderPickup, id = id)
			formatedDate = order.created_at.strftime("%Y-%m-%d %H:%M:%S")
			data_pickup = model_to_dict(get_object_or_404(OrderPickup, id = id))

			try :
				jenis_barang = JenisKiriman.objects.get(id=int(data_pickup['jenis_barang']))
				data_pickup['jenis_barang'] = jenis_barang.nama.capitalize()
				data_pickup['jenis_barang_id'] = jenis_barang.id
			except Exception as e:
				try :
					jenis_barang = JenisKiriman.objects.get(nama__iexact=data_pickup['jenis_barang'])
					data_pickup['jenis_barang'] = jenis_barang.nama.capitalize()
					data_pickup['jenis_barang_id'] = jenis_barang.id
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
				kurirPickup = User.objects.get(id=data_pickup['kurir_id'])
				data_pickup['kurir_nama'] = str(kurirPickup.first_name) +" || "+ str(kurirPickup.username)
			except :
				try :
					data_pickup['kurir_nama'] = 'Nama tidak diketahui, Silahkan update kembali'
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

			try :
				data_gudang = model_to_dict(get_object_or_404(Gudang, id = data_pickup['id_gudang']))
			except :
				data_gudang = {'nama_gudang' : '-'}

			try :
				data_pengemasan = model_to_dict(get_object_or_404(Pengemasan, id = data_pickup['id_pengemasan']))
			except :
				data_pengemasan = {'nama_pengemasan' : 'Tidak ada Pengemasan'}

			return JsonResponse({'order_pickup': data_pickup, 'pelanggan': data_pelanggan, 'pengemasan': data_pengemasan, 'gudang': data_gudang, 'tgl_order': formatedDate, 'msg': 'Berhasil Mengambil Data Order Pickup', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data Order Pickup, {}'.format(e), 'type': 'error'})

	def post(self, request, id):

		try:
			obj=OrderPickup.objects.filter(id=id)
			status_order = request.POST.get('status')
			obj.update(status=status_order)
			return JsonResponse({'msg': 'Berhasil Update Order Pickup', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Update Order Pickup', 'type': 'error' })