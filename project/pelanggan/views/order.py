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
from .order_pickup_ambil_data import *
from django.http import HttpResponse
from ekspedisi.views.pengiriman_ambil_data import ambil_data as ambil_data_pengiriman, ambil_rute as ambil_rute_pengiriman, ambil_kurir, ambil_status
from ekspedisi.views.print2pdf import render_to_pdf, render_barcode, render_qrcode
from ekspedisi.views.custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class GenerateInvoicePdf(View):
	def get(self, request, id, *args, **kwargs):
		try:
			pengiriman = ambil_data_pengiriman(get_object_or_404(Pengiriman, id=id))
			rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).first()
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).values()
			# print(list(log_pengiriman))

			if rute_pengiriman.id_kurir:
				kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=rute_pengiriman.id_kurir.id))
			else:
				kurir_pengiriman = ambil_kurir('')
			rute = ambil_rute_pengiriman(rute_pengiriman)
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).order_by('-created_at')[0])
			data = {'data': pengiriman, 'rute': rute, 'kurir': kurir_pengiriman, 'status': status_pengiriman, 'log': list(log_pengiriman)}
			pdf = render_to_pdf('pengiriman/print_billing.html', data)
			return HttpResponse(pdf, content_type='application/pdf')

		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data pengiriman, {}'.format(e), 'type': 'error'}, status=422)

class GenerateLabelPdf(View):
	def get(self, request, id, *args, **kwargs):
		try:
			pengiriman = ambil_data_pengiriman(get_object_or_404(Pengiriman, id=id))
			uri = 'https://' if request.is_secure() else 'http://'
			uri = uri + '{host}/track?type=qrcode&resi={id_pengiriman}'.format(host=str(request.META['HTTP_HOST']), id_pengiriman=pengiriman['id_pengiriman'])
			qrcode = render_qrcode(uri)
			barcode = render_barcode(pengiriman['id_pengiriman'])
			rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).first()
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).values()
			# print(list(log_pengiriman))

			if rute_pengiriman.id_kurir:
				kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=rute_pengiriman.id_kurir.id))
			else:
				kurir_pengiriman = ambil_kurir('')
			rute = ambil_rute_pengiriman(rute_pengiriman)
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).order_by('-created_at')[0])
			data = {'user': request.user,'qrcode': qrcode, 'barcode': barcode, 'data': pengiriman, 'rute': rute, 'kurir': kurir_pengiriman, 'status': status_pengiriman, 'log': list(log_pengiriman)}
			pdf = render_to_pdf('pengiriman/print_label.html', data)
			return HttpResponse(pdf, content_type='application/pdf')

		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data pengiriman, {}'.format(e), 'type': 'error'}, status=422)

@method_decorator(login_required(login_url='/order/login'), name='get')
class OrderPengirimanView(View):
	@method_decorator(user_customer_check(path_url='/order/login/'))
	def get(self, request):
		status_pengiriman = request.GET.get('status_pengiriman')
		form = PengirimanForm()
		form_pos = POSForm()
		data_list = []
		data_pengiriman = []
		
		current_user = request.user
		order_id = list(OrderPickup.objects.values().filter(is_active = False, status='done', id_customer=current_user.id).values_list('id', flat=True))
		pengiriman = Pengiriman.objects.filter(order_pickup_id__in=order_id).exclude(log_pengiriman__status_pengiriman='done').values()
		# print(pengiriman)

		i = 1
		for data in pengiriman:
			button_bukti_foto = ''
			status_terakhir = ''
			if_any_done = []
			data_list = [i]
			# GET ORDER ID
			try:
				order_id_pengiriman = OrderPickup.objects.get(id=data['order_pickup_id']).id_order
			except Exception as e:
				order_id_pengiriman = '-'
			# GET LAYANAN 
			try:
				layanan_pengiriman = Layanan.objects.get(id=data['layanan_id']).nama_layanan
			except Exception as e:
				layanan_pengiriman = '-'
			# GET LAST STATUS
			try :
				data_log = LogPengiriman.objects.filter(id_pengiriman=data['id']).latest('created_at')
				if data_log :
					status_terakhir = data_log.status_pengiriman.upper()
			except Exception as e:
				status_terakhir = '-'

			data_list.append(order_id_pengiriman)
			data_list.append(data['id_pengiriman'])
			data_list.append("<div class='text-center'>"+layanan_pengiriman+"</div>")
			data_list.append("<div class='text-center'>"+status_terakhir+"</div>")
			data_list.append(data['alamat_penerima'])
			data_list.append('<center><div class="btn-group" role="group">'+ button_bukti_foto +'<a href="'+ str(data['id']) +'/print_billing/" data-toggle="tooltip" title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm downloadBillingPengiriman" target="_blank"><i class="fa fa-fw fa-file"></i></a> <a href="'+ str(data['id']) +'/print_label/" data-toggle="tooltip" title="Label/Resi" data-id="' + str(data['id']) + '" class="Outlet Denpasar (panjer)btn btn-warning btn-sm downloadLabelX" target="_blank"><i class="fa fa-fw fa-qrcode"></i></a></div></center>')
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Pengiriman" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailPengiriman"><i class="fa fa-fw fa-eye"></i>&nbsp; Detail</a></div></center>')

			i =  i+1
			data_pengiriman.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_pengiriman}, status=200);

		# return render(request, 'pengiriman/index.html', context={'form': form, 'form_pos':POSForm, 'pengiriman': data_pengiriman})

class OrderPengirimanDoneView(View):
	@method_decorator(user_customer_check(path_url='/order/login/'))
	def get(self, request):
		status_pengiriman = request.GET.get('status_pengiriman')
		form = PengirimanForm()
		form_pos = POSForm()
		data_list = []
		data_pengiriman = []
		
		current_user = request.user
		order_id = list(OrderPickup.objects.values().filter(is_active = False, status='done', id_customer=current_user.id).values_list('id', flat=True))
		pengiriman = Pengiriman.objects.filter(order_pickup_id__in=order_id, log_pengiriman__status_pengiriman='done').values()
		# print(pengiriman)

		i = 1
		for data in pengiriman:
			button_bukti_foto =  '<a href="javascript:void(0)" data-id="' + str(data['id']) + '" title="Lihat Bukti Tanda Terima" class="btn btn-success btn-sm buttonTTD"><i class="fa fa-fw fa-image"></i></a>'
			status_terakhir = ''
			if_any_done = []
			data_list = [i]
			# GET ORDER ID
			try:
				order_id_pengiriman = OrderPickup.objects.get(id=data['order_pickup_id']).id_order
			except Exception as e:
				order_id_pengiriman = '-'
			# GET LAYANAN 
			try:
				layanan_pengiriman = Layanan.objects.get(id=data['layanan_id']).nama_layanan
			except Exception as e:
				layanan_pengiriman = '-'
			# GET LAST STATUS
			try :
				data_log = LogPengiriman.objects.filter(id_pengiriman=data['id']).latest('created_at')
				if data_log :
					status_terakhir = data_log.status_pengiriman.upper()
			except Exception as e:
				status_terakhir = '-'

			data_list.append(order_id_pengiriman)
			data_list.append(data['id_pengiriman'])
			data_list.append("<div class='text-center'>"+layanan_pengiriman+"</div>")
			data_list.append("<div class='text-center'>"+status_terakhir+"</div>")
			data_list.append(data['alamat_penerima'])
			data_list.append('<center><div class="btn-group" role="group">'+ button_bukti_foto +'<a href="'+ str(data['id']) +'/print_billing/" data-toggle="tooltip" title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm downloadBillingPengiriman" target="_blank"><i class="fa fa-fw fa-file"></i></a> <a href="'+ str(data['id']) +'/print_label/" data-toggle="tooltip" title="Label/Resi" data-id="' + str(data['id']) + '" class="Outlet Denpasar (panjer)btn btn-warning btn-sm downloadLabelX" target="_blank"><i class="fa fa-fw fa-qrcode"></i></a></div></center>')
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Pengiriman" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailPengiriman"><i class="fa fa-fw fa-eye"></i>&nbsp; Detail</a></div></center>')

			i =  i+1
			data_pengiriman.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_pengiriman}, status=200);

		# return render(request, 'pengiriman/index.html', context={'form': form, 'form_pos':POSForm, 'pengiriman': data_pengiriman})

class PelangganOrderBilling(View):
	@method_decorator(user_customer_check(path_url='/order/login/'))
	def get(self, request, id):
		try:
			order = get_object_or_404(OrderPickup, id = id)
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

@method_decorator(login_required(login_url='/order/login'), name='get')
class PelangganOrderView(View):
	@method_decorator(user_customer_check(path_url='/order/login/'))
	def get(self,request):
		try:
			form_pengiriman = PengirimanForm()
			form = PelangganOrderPickupForm()
			current_user = request.user
			datas = list(OrderPickup.objects.values().filter(is_active = True, id_customer=current_user.id))
			data_list = []
			data_order = []
			i = 1
			for data in datas:
				data_list = [i]
				try:
					layanan = get_object_or_404(Layanan, id = data['jenis_pengiriman_id'])
					jenis_pengiriman = layanan.nama_layanan
				except:
					jenis_pengiriman = ''

				data_list.append(data['id_order'])
				data_list.append(jenis_pengiriman)

				if data['status'] == 'waiting':
					data_list.append('<span class="badge badge-warning">'+data['status']+'</span><br>')
				else:
					if data['status'] == 'pickup':
						try:
							kurir_pickup = get_object_or_404(User, id = data['kurir_id_id'])
							pickup_by = 'by ' + kurir_pickup.first_name
						except Exception as e:
							pickup_by = '{}'.format(e)
					data_list.append('<span class="badge badge-info">'+data['status']+'</span><br>'+pickup_by)

				data_list.append(data['alamat_penerima'])
				data_list.append('<center><a href="javascript:void(0)" data-toggle="tooltip" title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-warning btn-sm downloadBilling"><i class="fa fa-fw fa-file-alt"></i></a></center>')
				if data['status'] == 'waiting':
					data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Lihat Detail" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrder"><i class="fa fa-fw fa-eye"></i> Detail</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Order" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editOrder"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Cancel Order" data-id="' + str(data['id']) + '" data-nama="' + str(data['id_order']) + '"class="btn btn-danger btn-sm cancelOrder"><i class="fa fa-fw fa-trash-alt"></i> Cancel</a></div><center>')
				elif data['status'] == 'done' or data['status'] == 'cancel':
					data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Lihat Detail" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrder"><i class="fa fa-fw fa-eye"></i> Detail</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Cancel Order" data-id="' + str(data['id']) + '" data-nama="' + str(data['id_order']) + '"class="btn btn-danger btn-sm deleteOrder"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div><center>')
				else:
					data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Lihat Detail" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrder"><i class="fa fa-fw fa-eye"></i> Detail</a></div><center>')

				i =  i+1
				data_order.extend([data_list])
			if request.is_ajax():
				return JsonResponse({'data': data_order, 'msg': 'Sukses Mengambil data', 'type': 'success'}, status=200)

		except Exception as e:
			return JsonResponse({'data': '', 'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})

		return render(request, 'frontend_pelanggan/templates/order/index.html', {'form':form, 'form_pengiriman':form_pengiriman})

	def post(self, request):
		try : 
			form = PelangganOrderPickupForm(request.POST)
			if form.is_valid():
				try:
					new_order = form.save(commit=False)
					# print(new_order.id_customer.alamat, request.POST)
					# return
					new_order.id_order = generate_id('OP', 8)
					if request.POST.get('alamat_pengirim_alt') :
						new_order.alamat_pengirim_alt = request.POST.get('alamat_pengirim_alt', 'Alamat default')
					else :
						try :
							new_order.alamat_pengirim_alt = new_order.id_customer.alamat
						except :
							pass
					new_order.save()
					data = model_to_dict(new_order)
					
					return JsonResponse({'data': data, 'msg': 'Berhasil Menambah Order Pickup', 'type': 'success'}, status=200)
				except Exception as e :
					return JsonResponse({'msg': 'Gagal Menambah Order Pickup {}'.format(e), 'type': 'error'}, status=400)
			else:
				print(form.errors)
				error = [er[0] for er in form.errors.values()]
				error = "<br> ".join(error)
				return JsonResponse({'msg': 'Mohon di cek kembali semua kelengkapan dan format data pada setiap kolom'.format(error), 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class PelangganOrderHistoryView(View):
	@method_decorator(user_customer_check(path_url='/order/login/'))
	def get(self,request):
		try:
			form = PelangganOrderPickupForm()
			current_user = request.user
			datas = list(OrderPickup.objects.values().filter(is_active = False, id_customer=current_user.id))
			data_list = []
			data_order = []
			i = 1
			for data in datas:
				data_list = [i]
				try:
					layanan = get_object_or_404(Layanan, id = data['jenis_pengiriman_id'])
					jenis_pengiriman = layanan.nama_layanan
				except:
					jenis_pengiriman = ''

				data_list.append(data['id_order'])
				data_list.append(jenis_pengiriman)

				if data['status'] == 'cancel':
					data_list.append('<span class="badge badge-danger">'+data['status']+'</span><br>')
				elif data['status'] == 'done':
					data_list.append('<span class="badge badge-success">'+data['status']+'</span><br>')
				else:
					data_list.append('<span class="badge badge-info">'+data['status']+'</span><br>')

				data_list.append(data['alamat_penerima'])
				if data['status'] == 'waiting':
					data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Lihat Detail" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrder"><i class="fa fa-fw fa-eye"></i> Detail</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Edit Order" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editOrder"><i class="fa fa-fw fa-edit"></i> Edit</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Cancel Order" data-id="' + str(data['id']) + '" data-nama="' + str(data['id_order']) + '"class="btn btn-danger btn-sm cancelOrder"><i class="fa fa-fw fa-trash-alt"></i> Cancel</a></div><center>')
				elif data['status'] == 'done' or data['status'] == 'cancel':
					data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Lihat Detail" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrder"><i class="fa fa-fw fa-eye"></i> Detail</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Cancel Order" data-id="' + str(data['id']) + '" data-nama="' + str(data['id_order']) + '"class="btn btn-danger btn-sm deleteOrder"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div><center>')
				else:
					data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Lihat Detail" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailOrder"><i class="fa fa-fw fa-eye"></i> Detail</a></div><center>')

				i =  i+1
				data_order.extend([data_list])
			if request.is_ajax():
				return JsonResponse({'data': data_order, 'msg': 'Sukses Mengambil data', 'type': 'success'}, status=200)

		except Exception as e:
			return JsonResponse({'data': '', 'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})

		return render(request, 'frontend_pelanggan/templates/order/index.html', {'form':form})

class PelangganOrderCancel(View):
	def post(self, request):
		try:
			QueryDict = request.POST
			id_cancel = QueryDict.get("id")
			keterangan = QueryDict.get("keterangan")
			order = OrderPickup.objects.get(id=id_cancel)
			order.keterangan_cancel = keterangan
			order.status = 'cancel'
			order.is_active = False
			order.save()
			return JsonResponse({'msg': 'Berhasil Cancel Order', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Meng-Cancel Order, {}'.format(e), 'type': 'error'}, status=443)


class PelangganOrderDelete(View):
	def post(self, request):
		try:
			QueryDict = request.POST
			id_delete = QueryDict.get("id")
			order = OrderPickup.objects.get(id=id_delete)
			order.is_active = False;
			order.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Order', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=443)

class PelangganOrderDetail(View):
	def get(self, request, id):
		try:
			data = ambil_data(get_object_or_404(OrderPickup, id=id))
			try :
				jenis_barang = JenisKiriman.objects.get(id=int(data['jenis_barang']))
				data['jenis_barang'] = jenis_barang.nama.capitalize()
				data['jenis_barang_id'] = jenis_barang.id
			except Exception as e:
				try :
					jenis_barang = JenisKiriman.objects.get(nama__iexact=data['jenis_barang'])
					data['jenis_barang'] = jenis_barang.nama.capitalize()
					data['jenis_barang_id'] = jenis_barang.id
				except :
					pass

			rute = ambil_rute(get_object_or_404(OrderPickup, id=id))
			return JsonResponse({'data':data, 'rute':rute, 'msg': 'Berhasil Ambil detail data', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'data': '', 'rute':'', 'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=443)

class PelangganOrderUpdate(View):
	def post(self, request):
		try : 
			obj = get_object_or_404(OrderPickup, id = request.POST.get("id"))
			form = PelangganOrderPickupForm(request.POST or None, instance = obj)
			if form.is_valid():
				try:
					new_order = form.save(commit=False)
					if request.POST.get('alamat_pengirim_alt') :
						new_order.alamat_pengirim_alt = request.POST.get('alamat_pengirim_alt', 'Alamat default')
					else :
						try :
							new_order.alamat_pengirim_alt = new_order.id_customer.alamat
						except :
							pass
					new_order.save();
					
					return JsonResponse({'msg': 'Berhasil Mengupdate Order Pickup', 'type': 'success'}, status=200)
				except Exception as e :
					return JsonResponse({'msg': 'Gagal Mengupdate Order Pickup {}'.format(e), 'type': 'error'}, status=400)
			else:
				print(form.errors)
				print(request.POST)
				error = [er[0] for er in form.errors.values()]
				error = "<br> ".join(error)
				return JsonResponse({'msg': 'Gagal, Form Order Pickup Tidak Valid, Pastikan semua data sudah terisi', 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class PelangganOrderLogin(View):
	def get(self, request):
		return render(request, 'frontend_pelanggan/templates/order/login.html')