from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import datetime, pytz
from datetime import timedelta
from random import randint
from django.utils import timezone

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from ekspedisi.models import *
from ekspedisi.forms import *
import math

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from ekspedisi.views.pengiriman_ambil_data import *


def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class KurirOrderPickupView(View):
	def get(self, request):
		order_berhasil = OrderPickup.objects.filter(kurir_id=request.user, is_active=False, status__iexact='done').select_related('orderpickup_pengiriman').values('id_order', 'created_at', 'orderpickup_pengiriman__id_pengiriman')
		try :
			hasil_pencarian = None
			data_filter_as_dict = {}
			if request.GET :
				hasil_pencarian = 'Hasil Pencarian anda'
				search_by = request.GET.get('search-by')
				search_value = request.GET.get('search-value', '')
				if search_by and search_value :
					data_filter_as_dict.update({search_by:search_value})
				orderstart = request.GET.get('orderstart', '')
				orderend = request.GET.get('orderend', '')
				if orderstart and orderend :
					data_filter_as_dict.update({'created_at__range':[datetime.datetime.strptime(orderstart, "%Y-%m-%d"),datetime.datetime.strptime(orderend, "%Y-%m-%d")]})
			# print(data_filter_as_dict)
			order = OrderPickup.objects.filter(is_active=True, id_toko_id=request.user.penempatan_toko.id, kurir_id=request.user, **data_filter_as_dict)
			# print(order.query)
		except Exception as e:
			print(e)
			order = {}
		context = {
			'is_active_order' : 'active',
			'order' : order,
			'order_berhasil': order_berhasil,
			'pencarian':hasil_pencarian
		}
		return render(request, 'mobile_kurir/templates/order_pickup/index.html', context)

class KurirOrderDetailView(View):
	def get(self, request, id):
		try:
			try :
				id = OrderPickup.objects.get(id=id)
				id = id.pk
			except Exception as e:
				id = Pengiriman.objects.get(id_order=id)
				id = id.pk

			order = get_object_or_404(OrderPickup, id=id)
			return render(request, 'mobile_kurir/templates/order_pickup/detail_pickup.html', context={
				'data':order,
				'is_active_order':'active'
			})
		except Exception as e:
			storage = messages.get_messages(request)
			storage.used = True
			pesan = str(e)
			messages.warning(request, pesan)
			return redirect('kurir_order_pickup')

	def post(self, request, id):
		try: 
			obj = get_object_or_404(Pengiriman, id=id)
		except Exception as e :
			print(e)

class KurirOrderDetailViewReadOnly(View):
	def get(self, request, id):
		try:
			try :
				id = OrderPickup.objects.get(id=id)
				id = id.pk
			except Exception as e:
				id = Pengiriman.objects.get(id_order=id)
				id = id.pk

			order = get_object_or_404(OrderPickup, id=id)
			return render(request, 'mobile_kurir/templates/order_pickup/detail_order.html', context={
				'data':order,
				'is_active_order':'active'
			})
		except Exception as e:
			storage = messages.get_messages(request)
			storage.used = True
			pesan = str(e)
			messages.warning(request, pesan)
			return redirect('kurir_dashboard')

class KurirUpdateOrderView(View):
	def post(self, request):
		try: 
			id_order = request.POST.get('id_order')
			status = request.POST.get('status_order')
			keterangan_cancel = request.POST.get('keterangan_cancel')
			if not status :
				return JsonResponse({'msg': 'Tidak dapat membaca status yang dikirimkan, invalid request', 'type': 'error', 'title':'Error'}, status=400)

			cek_status_order = OrderPickup.objects.filter(id_order=id_order)
			if cek_status_order.exists() :
				cek_kurir = cek_status_order.first().kurir_id_id
				try :
					yang_pickup = request.user.id
				except Exception as e:
					return JsonResponse({'msg': 'Gagal memperoleh penempatan toko, {}'.format("Silahkan periksa data kurir / admin"), 'type': 'error', 'title':'Error'}, status=400)
					
				if not cek_kurir :
					return JsonResponse({'msg': 'Belum ada kurir yang di assign untuk order pickup', 'type': 'error', 'title':'Error'}, status=400)
				elif cek_kurir and cek_kurir != yang_pickup :
					return JsonResponse({'msg': 'Kurir tidak sesuai, order pickup tidak dapat dilakukan', 'type': 'error', 'title':'Error'}, status=400)


				cek_status_order = cek_status_order.first().status
				if not cek_status_order.strip() == 'cancel' and not cek_status_order.strip() == 'done' :

					if status == 'cancel' :
						update = OrderPickup.objects.filter(id_order=id_order).update(status=status, keterangan_cancel=keterangan_cancel, is_active=False, kurir_id=request.user)
					else :
						order = OrderPickup.objects.filter(id_order=id_order)
						order_valid = order.first()
						try :
							yang_pickup = request.user.penempatan_toko
						except Exception as e:
							return JsonResponse({'msg': 'Gagal memperoleh penempatan toko, {}'.format("Silahkan periksa data kurir / admin"), 'type': 'error', 'title':'Error'}, status=400)
						
						try:
							if order_valid.id_pengemasan.id:
								data_pengemasan = order_valid.id_pengemasan.id
							else:
								data_pengemasan = None
						except:
							data_pengemasan = None

						try:
							print(order_valid.satuan.id)
							if order_valid.satuan.id:
								data_satuan = order_valid.satuan.id
							else:
								data_satuan = None
						except:
							data_satuan = None

						print('INI ADALAH DATA ORDER', str("{:.1f}".format(float(order_valid.berat))))
						berat_ons_order = int(str("{:.1f}".format(float(order_valid.berat))[-1:]))
						if berat_ons_order >= 1 :
							berat_order = math.floor(float(str("{:.1f}".format(float(order_valid.berat))))) + 1 
						else :
							berat_order = math.floor(float(str("{:.1f}".format(float(order_valid.berat)))))
						# print(data_satuan)

						data_pengiriman = {
							'outlet_pengiriman':yang_pickup,
							'gudang_pengiriman':order_valid.id_gudang_id,
							'nama_pengirim':order_valid.id_customer.first_name,
							'status_pengirim':order_valid.id_customer.register_sebagai, 
							'no_telp_pengirim':order_valid.id_customer.no_telp, 
							'email_pengirim':order_valid.id_customer.email, 
							# 'alamat_pengirim':order_valid.id_customer.alamat,
							'alamat_pengirim':order_valid.alamat_pengirim_alt if order_valid.alamat_pengirim_alt else order_valid.id_customer.alamat,
							
							'provinsi_pengirim':order_valid.provinsi_pengirim,
							'kota_pengirim':order_valid.kota_pengirim, 
							'kecamatan_pengirim':order_valid.kecamatan_pengirim,
							'desa_pengirim':order_valid.desa_pengirim,
							'kode_pos_pengirim':order_valid.kode_pos_pengirim,
							
							'nama_penerima':order_valid.nama_penerima,
							'no_telp_penerima':order_valid.no_tlp_penerima,
							'email_penerima':order_valid.email_penerima,
							'alamat_penerima':order_valid.alamat_penerima,
							
							'provinsi_penerima':order_valid.provinsi_penerima,
							'kota_penerima':order_valid.kota_penerima,
							'kecamatan_penerima':order_valid.kecamatan_penerima,
							'desa_penerima':order_valid.desa_penerima,
							'kode_pos_penerima':order_valid.kode_pos_penerima,
							
							'outlet_penerimaan':order_valid.id_toko2,
							'gudang_penerimaan':order_valid.id_gudang2,
							'jenis_barang':order_valid.jenis_barang,
							'detail_barang':order_valid.detail_barang,
							'pengemasan':data_pengemasan,
							'layanan':order_valid.jenis_pengiriman,
							'jumlah':order_valid.jumlah,
							'satuan':data_satuan,
							'berat':berat_order,
							'pencatat':request.user,
							'tarif_berat':order_valid.tarif_berat,
							'tarif_kilometer':order_valid.tarif_kilometer,
							'tarif_gudang':order_valid.tarif_gudang,
							'tarif_layanan':order_valid.tarif_layanan,
							'total_tarif':order_valid.total_tarif,
						}

						

						form = PengirimanForm(data=data_pengiriman)

						if form.is_valid() :
							update = order.update(status=status, id_toko=yang_pickup, keterangan_cancel=None, is_active=False, kurir_id=request.user)
							new_pengiriman = form.save(commit=False)
							new_pengiriman.id_pengiriman = generate_id('ER', 8)
							new_pengiriman.source = 'order_pickup'
							new_pengiriman.order_pickup_id = order_valid.id
							new_pengiriman.save()

							data_pos ={
							'id_pengiriman': new_pengiriman.id_pengiriman,
							'nominal_bayar': new_pengiriman.total_tarif,
							'total_tagihan': new_pengiriman.total_tarif,
							'total_kembali': 0
							}

							try:
								# print(new_pengiriman.id_pengiriman)
								form_pos = POSForm()
								new_pos = form_pos.save(commit=False)
								new_pos.id_pengiriman = new_pengiriman
								new_pos.nominal_bayar = new_pengiriman.total_tarif
								new_pos.total_tagihan = new_pengiriman.total_tarif
								new_pos.total_kembali = 0
								new_pos.no_transaksi = generate_id('EP', 8)
								new_pos.save();
							except Exception as e:
								print('Terjadi Kesalahan POS, {}'.format(str(e)))

							formPelacakan = LogPengirimanForm()
							new_pelacakan = formPelacakan.save(commit=False)
							new_pelacakan.id_pengiriman = get_object_or_404(Pengiriman, id_pengiriman=new_pengiriman)
							new_pelacakan.rute_pengiriman_outlet = get_object_or_404(Toko, id=yang_pickup.id)
							new_pelacakan.rute_pengiriman_outlet_akhir = get_object_or_404(Toko, id=order_valid.id_toko2_id)
							new_pelacakan.rute_pengiriman_gudang = get_object_or_404(Gudang, id=order_valid.id_gudang_id)
							new_pelacakan.rute_pengiriman_gudang_akhir = get_object_or_404(Gudang, id=order_valid.id_gudang2_id)
							new_pelacakan.status_pengiriman = 'pickup_by'
							new_pelacakan.titik_lokasi = yang_pickup.titik_lokasi
							new_pelacakan.id_kurir_id = request.POST.get('id_kurir', 0)
							new_pelacakan.save()

						else :
							print(form.errors.items())
							error = []
							for data in form.errors.items() :
								error_is = "{} : {}".format(data[0],data[1][0])
								error.append(error_is)
							error = "<br> ".join(error)
							return JsonResponse({'msg': 'Gagal, Data pengiriman Tidak Valid <br> Silahkan periksa kembali data order dan kelengkapannya'.format(error), 'type': 'error', 'title':'Error'}, status=422)

					if update :
						return JsonResponse({'msg': 'Status order telah berhasil diubah', 'type': 'success', 'title':'Success'}, status=200)
					else :
						return JsonResponse({'msg': 'Tidak ada data yang diubah', 'type': 'info', 'title':'Informasi'}, status=200)
				else :
					return JsonResponse({'msg': 'Data order ini sudah di cancel atau di selesaikan (done) sebelumnya, tidak dapat mengubah status', 'type': 'info', 'title':'Informasi'}, status=200)
			else :
				return JsonResponse({'msg': 'Data order tidak dapat ditemukan, silahkan ulangi kembali', 'type': 'error', 'title':'Error'}, status=400)

		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(str(e)), 'type': 'error', 'title':'Error'}, status=400)