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
from django.utils.timezone import get_current_timezone, make_aware, now
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.db.models import Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.forms.models import model_to_dict

from .pengiriman_ambil_data import *
from .custom_decorator import *
from .print2pdf import render_to_pdf, render_barcode, render_qrcode

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class PengirimanPilihOutletGudangManual(View) :
	@csrf_exempt
	def post(self, request):
		if request.is_ajax() :
			try : 
				outlet_pengirim = {}
				outlet_penerima = {}
				gudang_pengirim = {}
				gudang_penerima = {}

				kec_pengirim = request.POST.get('kecamatan_pengirim', False)
				id_outlet_pengirim = request.POST.get('id_outlet_pengirim', False)
				kec_penerima = request.POST.get('kecamatan_penerima', False)
				if kec_pengirim and kec_penerima and id_outlet_pengirim:
					outlet_pengirim = Toko.objects.filter(is_active=True, id=id_outlet_pengirim).values('id', 'nama_toko', 'kecamatan_toko_id').first() if Toko.objects.filter(is_active=True, id=id_outlet_pengirim).values('id', 'nama_toko') else {}
					if outlet_pengirim :
						gudang_pengirim = list(Gudang.objects.filter(is_active=True, kecamatan_gudang_id=outlet_pengirim['kecamatan_toko_id']).values('id', 'nama_gudang','alamat',kode_pos=F('kode_pos_gudang__kode_pos'),desa=F('desa_gudang__nama_desa'),kec=F('kecamatan_gudang__nama_kecamatan'),kota=F('kota_gudang__nama_kota'),provinsi=F('provinsi_gudang__nama_provinsi'))) if Gudang.objects.filter(is_active=True, kecamatan_gudang_id=outlet_pengirim['kecamatan_toko_id']).values('id', 'nama_gudang') else {}

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


@method_decorator(login_required, name='get')
class PengirimanView(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		status_pengiriman = request.GET.get('status_pengiriman')
		form = PengirimanForm()
		form_pos = POSForm()
		data_list = []
		data_pengiriman = []
		outlet_tugas = 0
		is_gudang = False
		outlet_tugas = 0
		gudang_tugas = 0

		if request.user.is_authenticated:
			is_admin = request.user.is_superuser
		else:
			is_admin = False

		if is_admin:
			pengiriman = list(Pengiriman.objects.filter(is_active=True).order_by("-pk").values())
			if status_pengiriman and status_pengiriman == '1' :
				pengiriman = list(Pengiriman.objects.filter(is_active=True, log_pengiriman__status_pengiriman='done').order_by("-pk").values())
			elif status_pengiriman and status_pengiriman == '0' :
				pengiriman = list(Pengiriman.objects.filter(is_active=True).exclude(log_pengiriman__status_pengiriman='done').order_by("-pk").values())

		else:
			try:
				if request.user.penempatan_toko.id :
					outlet_tugas = request.user.penempatan_toko.id
				else :
					outlet_tugas = False
			except:
				outlet_tugas = False
			try:
				if request.user.penempatan_gudang.id :
					gudang_tugas = request.user.penempatan_gudang.id
					is_gudang = True
				else :
					gudang_tugas = False
					is_gudang = False
			except:
				gudang_tugas = False
				is_gudang = False

			if outlet_tugas :
				pengiriman = list(Pengiriman.objects.filter(Q(is_active=True) & Q(Q(log_pengiriman__id_kurir__penempatan_toko_id=outlet_tugas) | Q(outlet_pengiriman_id=outlet_tugas))).order_by("-pk").distinct().values())
				if status_pengiriman and status_pengiriman == '1' :
					data_log =  LogPengiriman.objects.filter(Q(Q(id_kurir__penempatan_toko_id=outlet_tugas) | Q(id_pengiriman__outlet_pengiriman_id=outlet_tugas)), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
					# pengiriman = list(Pengiriman.objects.filter(Q(is_active=True) & Q(Q(log_pengiriman__id_kurir__penempatan_toko_id=outlet_tugas) | Q(outlet_pengiriman_id=outlet_tugas)) & Q(log_pengiriman__status_pengiriman='done')).order_by("-pk").distinct().values())
					pengiriman = list(Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').order_by('-pk').distinct().values())
				elif status_pengiriman and status_pengiriman == '0' :
					pengiriman = list(Pengiriman.objects.filter(Q(is_active=True) & Q(Q(log_pengiriman__id_kurir__penempatan_toko_id=outlet_tugas) | Q(outlet_pengiriman_id=outlet_tugas))).exclude(log_pengiriman__status_pengiriman='done').order_by("-pk").distinct().values())
			elif gudang_tugas :
				pengiriman = list(Pengiriman.objects.filter(Q(is_active=True) & Q(log_pengiriman__id_kurir__penempatan_gudang_id=gudang_tugas)).order_by("-pk").distinct().values())
				if status_pengiriman and status_pengiriman == '1' :
					data_log =  LogPengiriman.objects.filter(Q(id_kurir__penempatan_gudang_id=gudang_tugas), id_pengiriman__is_active=True).values_list('id_pengiriman_id', flat=True).distinct()
					# pengiriman = list(Pengiriman.objects.filter(Q(is_active=True) & Q(log_pengiriman__id_kurir__penempatan_gudang_id=gudang_tugas) & Q(log_pengiriman__status_pengiriman='done')).order_by("-pk").distinct().values())
					pengiriman = list(Pengiriman.objects.filter(log_pengiriman__id_pengiriman_id__in=data_log, log_pengiriman__status_pengiriman='done').order_by('-pk').distinct().values())
				elif status_pengiriman and status_pengiriman == '0' :
					pengiriman = list(Pengiriman.objects.filter(Q(is_active=True) & Q(log_pengiriman__id_kurir__penempatan_gudang_id=gudang_tugas)).exclude(log_pengiriman__status_pengiriman='done').order_by("-pk").distinct().values())
		i = 1
		for data in pengiriman:
			button_bukti_foto = ''
			status_terakhir = ''
			if_any_done = []
			data_list = [i]
			data_list.append(data['id_pengiriman'])
			data_list.append(data['nama_pengirim'])
			try:
				data_log = LogPengiriman.objects.filter(id_pengiriman=data['id']).latest('created_at')
				if data_log :
					status_terakhir = data_log.status_pengiriman

				if_any_done = list(LogPengiriman.objects.filter(id_pengiriman=data['id']).values_list('status_pengiriman', flat=True))
				if data_log.id_kurir:
					kurir = get_object_or_404(User, id=data_log.id_kurir.id)
					data_list.append('<span class="badge badge-success">'+kurir.first_name.upper()+'</span><br>')
				else:
					data_list.append('<span class="badge badge-danger">Kosong</span><br>')
				if data_log.status_pengiriman:
					status_data = ''
					if data['outlet_pengiriman_id'] == outlet_tugas:
						status_data = '<span class="badge badge-success">Pengiriman Paket</span><br>'
					elif data['outlet_penerimaan_id'] == outlet_tugas:
						status_data = '<span class="badge badge-info">Penerimaan Paket</span><br>'
					else:
						status_data = ''
					status = data_log.status_pengiriman
					data_list.append(status_data + status.upper())
				else:
					data_list.append('WAITING')
			except Exception as e:
				data_list.append('Petugas~Log File Kosong')
				data_list.append('Status~Log File Kosong')
				
			if is_admin == True:
				button_delete = '<a href="javascript:void(0)" data-toggle="tooltip" title="Delete pengiriman" data-id="' + str(data['id']) + '" data-nama="RESI: ' + str(data['id_pengiriman'])+ ' Pengirim: ' + str(data['nama_pengirim']) + '"class="btn btn-danger btn-sm deletePengiriman"><i class="fa fa-fw fa-trash-alt"></i></a>'
			else:
				button_delete = ''

			if is_gudang == False:
				if 'done' not in if_any_done :
					if str(status_terakhir).lower() == 'waiting' :
						button_edit = '<a href="javascript:void(0)" data-toggle="tooltip" title="Edit pengiriman" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm editPengiriman"><i class="fa fa-fw fa-edit"></i></a>'
					else :
						button_edit = ''
				else :
					button_bukti_foto =  '<a href="javascript:void(0)" data-id="' + str(data['id']) + '" title="Lihat Bukti Tanda Terima" class="btn btn-success btn-sm buttonTTD"><i class="fa fa-fw fa-image"></i></a>'
					button_edit = ''
			else:
				button_edit = ''
		
			data_list.append('<center><div class="btn-group" role="group">'+ button_bukti_foto +'<a href="'+ str(data['id']) +'/print_billing/" data-toggle="tooltip" title="Download Billing" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm downloadBilling" target="_blank"><i class="fa fa-fw fa-file"></i></a> <a href="'+ str(data['id']) +'/print_label/" data-toggle="tooltip" title="Label/Resi" data-id="' + str(data['id']) + '" class="Outlet Denpasar (panjer)btn btn-warning btn-sm downloadLabelX"><i class="fa fa-fw fa-qrcode"></i></a></div></center>')

			if is_gudang or data['outlet_pengiriman_id'] != outlet_tugas and data['outlet_penerimaan_id'] == outlet_tugas or data['gudang_pengiriman_id'] != gudang_tugas and data['gudang_penerimaan_id'] == gudang_tugas :
				data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Pengiriman" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailPengiriman"><i class="fa fa-fw fa-eye"></i></a>')
			else :
				data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Pengiriman" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm detailPengiriman"><i class="fa fa-fw fa-eye"></i></a>'+button_edit+'<a href="javascript:void(0)" data-toggle="tooltip" title="Arsip pengiriman" data-id="' + str(data['id']) + '" data-nama="RESI: ' + str(data['id_pengiriman'])+ ' Pengirim: ' + str(data['nama_pengirim']) + '"class="btn btn-warning btn-sm arsipPengiriman"><i class="fa fa-fw fa-archive"></i></a>'+button_delete+'</div></center>')

			i =  i+1
			data_pengiriman.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_pengiriman}, status=200);

		return render(request, 'pengiriman/index.html', context={'form': form, 'form_pos':POSForm, 'pengiriman': data_pengiriman})

	@csrf_exempt
	def post(self, request):
		try : 
			form = PengirimanForm(request.POST)
			formPelacakan = LogPengirimanForm()
			if form.is_valid():
				try:
					tz = get_current_timezone()
					new_pengiriman = form.save(commit=False)
					new_pengiriman.id_pengiriman = generate_id('ER', 8)
					new_pengiriman.save()

					new_pelacakan = formPelacakan.save(commit=False)
					new_pelacakan.id_pengiriman = get_object_or_404(Pengiriman, id_pengiriman=new_pengiriman)
					new_pelacakan.rute_pengiriman_outlet = get_object_or_404(Toko, id=request.POST['outlet_pengiriman'])
					new_pelacakan.rute_pengiriman_outlet_akhir = get_object_or_404(Toko, id=request.POST['outlet_penerimaan'])
					new_pelacakan.rute_pengiriman_gudang = get_object_or_404(Gudang, id=request.POST['rute_pengiriman_gudang'])
					new_pelacakan.rute_pengiriman_gudang_akhir = get_object_or_404(Gudang, id=request.POST['rute_pengiriman_gudang_akhir'])
					new_pelacakan.status_pengiriman = 'waiting'
					new_pelacakan.save()
					data_to_return = {'id_pengiriman':new_pengiriman.id, 'total_tagihan':str(new_pengiriman.total_tarif)}

					return JsonResponse({'msg': 'Berhasil Menambah data pengiriman', 'data_pengiriman':data_to_return, 'type': 'success'}, status=200)
				except Exception as e :
					return JsonResponse({'msg': 'Gagal Menambah data pengiriman {}'.format(e), 'type': 'error'}, status=400)
			else:
				error = [er[0] for er in form.errors.values()]
				print(form.errors)
				error = "<br> ".join(error)
				return JsonResponse({'msg': 'Mohon di cek kembali semua kelengkapan dan format data pada setiap kolom'.format(error), 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class GenerateInvoicePdf(View):
	def get(self, request, id, *args, **kwargs):
		try:
			pengiriman = ambil_data(get_object_or_404(Pengiriman, id=id))
			rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).first()
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).values()
			# print(list(log_pengiriman))

			if rute_pengiriman.id_kurir:
				kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=rute_pengiriman.id_kurir.id))
			else:
				kurir_pengiriman = ambil_kurir('')
			rute = ambil_rute(rute_pengiriman)
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).order_by('-created_at')[0])
			data = {'data': pengiriman, 'rute': rute, 'kurir': kurir_pengiriman, 'status': status_pengiriman, 'log': list(log_pengiriman)}
			pdf = render_to_pdf('pengiriman/print_billing.html', data)
			return HttpResponse(pdf, content_type='application/pdf')

		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data pengiriman, {}'.format(e), 'type': 'error'}, status=422)


class GenerateLabelPdf(View):
	def get(self, request, id, *args, **kwargs):
		try:
			pengiriman = ambil_data(get_object_or_404(Pengiriman, id=id))
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
			rute = ambil_rute(rute_pengiriman)
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).order_by('-created_at')[0])
			data = {'user': request.user, 'qrcode': qrcode, 'barcode': barcode, 'data': pengiriman, 'rute': rute, 'kurir': kurir_pengiriman, 'status': status_pengiriman, 'log': list(log_pengiriman)}
			pdf = render_to_pdf('pengiriman/print_label.html', data)
			return HttpResponse(pdf, content_type='application/pdf')

		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data pengiriman, {}'.format(e), 'type': 'error'}, status=422)

class PengirimanArsipView(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = PengirimanForm()
		form_pos = POSForm()
		data_list = []
		data_pengiriman = []
		outlet_tugas = 0

		if request.user.is_authenticated:
			is_admin = request.user.is_superuser
		else:
			is_admin = False
				
		if is_admin:
			pengiriman = list(Pengiriman.objects.filter(is_active=False).order_by("-pk").values())
		else:
			try:
				outlet_tugas = request.user.penempatan_toko.id
			except:
				outlet_tugas = 0
			pengiriman = list(Pengiriman.objects.filter(Q(is_active=False) & Q(Q(outlet_pengiriman_id=outlet_tugas) | Q(outlet_penerimaan_id=outlet_tugas))).order_by("-pk").values())
		i = 1
		for data in pengiriman:
			data_list = [i]
			data_list.append(data['id_pengiriman'])
			data_list.append(data['nama_pengirim'])
			data_log = LogPengiriman.objects.filter(id_pengiriman=data['id'])
			if data_log :
				try :
					data_log = LogPengiriman.objects.filter(id_pengiriman=data['id']).latest('created_at')
					if data_log.id_kurir:
						kurir = get_object_or_404(User, id=data_log.id_kurir.id)
						data_list.append(kurir.first_name)
					else:
						data_list.append('Kosong')
					if data_log.status_pengiriman:
						status_data = ''
						if data['outlet_pengiriman_id'] == outlet_tugas:
							status_data = '<span class="badge badge-success">Pengiriman Paket</span><br>'
						elif data['outlet_penerimaan_id'] == outlet_tugas:
							status_data = '<span class="badge badge-info">Penerimaan Paket</span><br>'
						else:
							status_data = ''

						status = data_log.status_pengiriman
						data_list.append(status_data + status.upper())
					else:
						data_list.append('WAITING')
					data_list.append('<a href="'+ str(data['id']) +'/print_billing/" target="blank" data-toggle="tooltip" title="Billing Pengiriman" data-id="' + str(data['id']) + '" class="btn btn-warning btn-sm downloadBilling"><i class="fa fa-fw fa-file"></i> Unduh</a>')
					data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" title="Unarsip Pengiriman" data-id="' + str(data['id']) + '" class="btn btn-success btn-sm unarsipPengiriman"><i class="fa fa-fw fa-upload"></i> Restore</a></div></center>')
					i =  i+1
					data_pengiriman.extend([data_list])
				except :
					pass

		if request.is_ajax():
			return JsonResponse({'data': data_pengiriman}, status=200)
		return redirect('/pengiriman')

class PengirimanTandaTerima(View):
	def post(self, request, id):
		try:
			tandaterima = TandaTerima.objects.get(id_pengiriman_id=id)
			tandaterima = list(tandaterima.bukti_foto.all().values_list('foto', flat=True))
			if(tandaterima) :
				tandaterima = ['/media/'+bukti for bukti in tandaterima]
			else :
				tandaterima = []
			return JsonResponse({'msg': 'Berhasil Menghapus Data pengiriman', 'type': 'success', 'data':tandaterima}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengapus Data pengiriman {}'.format(e), 'type': 'error'}, status=400)

class PengirimanDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request, id):
		try:
			pengiriman = Pengiriman.objects.get(id=id)
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id) # => banyak log Pengiriman
			for log in log_pengiriman:
				log.delete()
			pengiriman.delete()
			return JsonResponse({'msg': 'Berhasil Menghapus Data pengiriman', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengapus Data pengiriman {}'.format(e), 'type': 'error'}, status=400)

class PengirimanArsip(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def post(self, request, id):

		pengiriman = Pengiriman.objects.get(id=id)
		log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id) # => banyak log Pengiriman
		if log_pengiriman.exists() :
			status = LogPengiriman.objects.filter(id_pengiriman=id).latest('created_at')
			if status.status_pengiriman == 'done':
				try:
					pengiriman.is_active = False
					pengiriman.save()
					for log in log_pengiriman:
						log.is_active = False
						log.save()
					return JsonResponse({'msg': 'Berhasil mengarsipkan data pengiriman', 'type': 'success'}, status=200)
				except:
					return JsonResponse({'msg': 'Gagal menghapus data pengiriman', 'type': 'error'}, status=400)
			else:
				return JsonResponse({'msg': 'Tidak Bisa Arsip!, Status Pengiriman BELUM Selesai/DONE', 'type': 'error'}, status=400)
		else :
			pengiriman.is_active = False
			pengiriman.save()
			return JsonResponse({'msg': 'Tidak dapat menemukan Log Pengiriman, namun tetap diarsipkan', 'type': 'error'}, status=200)


class PengirimanUnarsip(View):
	@method_decorator(user_admin_check(path_url='/page_not_found/'))
	def post(self, request, id):

		pengiriman = Pengiriman.objects.get(id=id)
		log_pengiriman = list(LogPengiriman.objects.filter(id_pengiriman=id).values_list('status_pengiriman', flat=True)) # => banyak log Pengiriman
		# status = LogPengiriman.objects.filter(id_pengiriman=id).latest('created_at')
		if 'done' in log_pengiriman:
			try:
				pengiriman.is_active = True
				pengiriman.save()
				# for log in log_pengiriman:
				# 	log.is_active = True
				# 	log.save()
				return JsonResponse({'msg': 'Berhasil Mengembalikan data pengiriman', 'type': 'success'}, status=200)
			except:
				return JsonResponse({'msg': 'Gagal Mengembalikan data pengiriman', 'type': 'error'}, status=400)
		else:
			return JsonResponse({'msg': 'Tidak Mengembalikan data pengiriman!, Status Pengiriman BELUM Selesai/DONE', 'type': 'error'}, status=400)

# 'provinsi_pengirim','kota_pengirim','kecamatan_pengirim','desa_pengirim','kode_pos_pengirim','provinsi_penerima','kota_penerima','kecamatan_penerima','desa_penerima','kode_pos_penerima','outlet_penerimaan','outlet_pengiriman','pengemasan','layanan', 'pencatat'
class PengirimanDetail(View):
	# @method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			pengiriman = ambil_data(get_object_or_404(Pengiriman, id=id))
			try :
				jenis_barang = JenisKiriman.objects.get(id=int(pengiriman['jenis_barang']))
				pengiriman['jenis_barang'] = jenis_barang.nama.capitalize()
				pengiriman['jenis_barang_id'] = jenis_barang.id
			except Exception as e:
				try :
					jenis_barang = JenisKiriman.objects.get(nama__iexact=pengiriman['jenis_barang'])
					pengiriman['jenis_barang'] = jenis_barang.nama.capitalize()
					pengiriman['jenis_barang_id'] = jenis_barang.id
				except :
					pass

			rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).first()
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).values('created_at', 'status_pengiriman', 'titik_lokasi', kurir_nama=F('id_kurir__first_name'), kurir_telp=F('id_kurir__no_telp'), kurir_penempatan_gudang=F('id_kurir__penempatan_gudang__nama_gudang'), kurir_penempatan_outlet=F('id_kurir__penempatan_toko__nama_toko'))
			# print(list(log_pengiriman))

			rute = ambil_rute(rute_pengiriman)
			status_pengiriman_terakhir = LogPengiriman.objects.filter(id_pengiriman=id).latest('created_at')
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).latest('created_at'))
			if status_pengiriman_terakhir.id_kurir:
				kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=status_pengiriman_terakhir.id_kurir.id))
			else:
				kurir_pengiriman = ambil_kurir('')
			print("Kurir terakhir SCAN", kurir_pengiriman)

			return JsonResponse({'data': pengiriman, 'rute': rute, 'kurir': kurir_pengiriman, 'status': status_pengiriman, 'log': list(log_pengiriman), 'msg': 'Berhasil Mengambil Data pengiriman', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data pengiriman, {}'.format(e), 'type': 'error'})

	def post(self, request, id):
		try: 
			obj = get_object_or_404(Pengiriman, id = id)
			form = PengirimanForm(request.POST or None, instance = obj)
			if form.is_valid():
				try:
					form.save()
						
					return JsonResponse({'msg': 'Berhasil Update data Pengiriman', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal Menambah data Pengiriman {}'.format(e), 'type': 'error'}, status=200)
			else:
				print(form.errors)
				return JsonResponse({'msg': 'Gagal Update data Pengiriman Form Tidak Valid', 'type': 'error'})
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'})

class PengirimanPOS(View):
	# @method_decorator(user_admin_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			pengiriman = ambil_data(get_object_or_404(Pengiriman, id=id))
			rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).first()
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).values()
			# print(list(log_pengiriman))

			if rute_pengiriman.id_kurir:
				kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=rute_pengiriman.id_kurir.id))
			else:
				kurir_pengiriman = ambil_kurir('')
			rute = ambil_rute(rute_pengiriman)
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).order_by('-created_at')[0])

			return JsonResponse({'data': pengiriman, 'rute': rute, 'kurir': kurir_pengiriman, 'status': status_pengiriman, 'log': list(log_pengiriman), 'msg': 'Berhasil Mengambil Data pengiriman', 'type': 'success'})
		except Exception as e:
			return JsonResponse({'msg': 'Gagal Mengambil Data pengiriman, {}'.format(e), 'type': 'error'})

	def post(self, request):
		try: 
			form = POSForm(request.POST)
			if form.is_valid():
				try:
					data_form = form.save(commit=False)
					data_form.no_transaksi = generate_id('EP', 8)
					data_form.save()
					return JsonResponse({'msg': 'Berhasil menyimpan data pembayaran', 'type': 'success'}, status=200)
				except Exception as e:
					return JsonResponse({'msg': 'Gagal menyimpan pembayaran, {}'.format(e), 'type': 'error'}, status=200)
			else:
				print(request.POST ,form.errors)
				return JsonResponse({'msg': 'Gagal update pembayaran, Form tidak valid', 'type': 'error'}, status=400)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=400)

class PengirimanPOSView(View) :
	def get(self, request) :
		_filter = False
		form = PengirimanForm()
		data_filter_as_dict = {}
		if request.GET :
			orderstart = request.GET.get('orderstart', '')
			orderend = request.GET.get('orderend', '')
			customer = request.GET.get('customer', '')
			noTransaksi = request.GET.get('noTransaksi', '')
			noResi = request.GET.get('noResi', '')
			jenisPelanggan = request.GET.get('jenisPelanggan', '')
			if (orderstart and orderend) or customer or noTransaksi or noResi or jenisPelanggan:
				_filter = True
				tz = get_current_timezone()
				# print(make_aware(datetime.datetime.combine(datetime.datetime.strptime(orderstart, "%Y-%m-%d"), datetime.time.min)))
				if orderstart and orderend and customer and noTransaksi and noResi and jenisPelanggan:
					data_filter_as_dict.update({
						'created_at__gte':datetime.datetime.combine(datetime.datetime.strptime(orderstart, "%Y-%m-%d"), datetime.time.min), 
						'created_at__lte':datetime.datetime.combine(datetime.datetime.strptime(orderend, "%Y-%m-%d"), datetime.time.max),
						'id_pengiriman__nama_pengirim__icontains': customer,
						'no_transaksi__icontains': noTransaksi,
						'id_pengiriman__id_pengiriman__icontains': noResi,
						'id_pengiriman__status_pengirim__icontains': jenisPelanggan,
						})
				elif orderstart and orderend:
					data_filter_as_dict.update({
						'created_at__gte':datetime.datetime.combine(datetime.datetime.strptime(orderstart, "%Y-%m-%d"), datetime.time.min), 
						'created_at__lte':datetime.datetime.combine(datetime.datetime.strptime(orderend, "%Y-%m-%d"), datetime.time.max)
						})
				elif orderstart and orderend and customer:
					data_filter_as_dict.update({
						'created_at__gte':datetime.datetime.combine(datetime.datetime.strptime(orderstart, "%Y-%m-%d"), datetime.time.min), 
						'created_at__lte':datetime.datetime.combine(datetime.datetime.strptime(orderend, "%Y-%m-%d"), datetime.time.max),
						'id_pengiriman__nama_pengirim__icontains': customer
						})
				elif noTransaksi and noResi and jenisPelanggan:
					data_filter_as_dict.update({
						'no_transaksi__icontains': noTransaksi,
						'id_pengiriman__id_pengiriman__icontains': noResi,
						'id_pengiriman__status_pengirim__icontains': jenisPelanggan,
						})
				elif noTransaksi and jenisPelanggan:
					data_filter_as_dict.update({
						'no_transaksi__icontains': noTransaksi,
						'id_pengiriman__status_pengirim__icontains': jenisPelanggan,
						})
				elif noResi and jenisPelanggan:
					data_filter_as_dict.update({
						'id_pengiriman__id_pengiriman__icontains': noResi,
						'id_pengiriman__status_pengirim__icontains': jenisPelanggan,
						})
				elif noTransaksi:
					data_filter_as_dict.update({
						'no_transaksi__icontains': noTransaksi,
						})
				elif noResi:
					data_filter_as_dict.update({
						'id_pengiriman__id_pengiriman__icontains': noResi,
						})
				elif jenisPelanggan:
					data_filter_as_dict.update({
						'id_pengiriman__status_pengirim__icontains': jenisPelanggan,
						})
				elif customer:
					data_filter_as_dict.update({
						'id_pengiriman__nama_pengirim__icontains': customer
						})
				else:
					data_filter_as_dict = {}
		print(data_filter_as_dict)
		pos = list(POS.objects.filter(is_active=True, **data_filter_as_dict).order_by('-created_at').values('id','created_at','id_pengiriman_id', 'no_transaksi', 'id_pengiriman__id_pengiriman', 'id_pengiriman__nama_pengirim', 'id_pengiriman__status_pengirim', 'total_tagihan', 'id_pengiriman__total_tarif'))
		print(POS.objects.filter(is_active=True, **data_filter_as_dict).query)
		data_list = []
		data_pos = []
		i = 1
		for data in pos:
			data_list = [i]
			data_list.append(datetime.datetime.strftime(data['created_at'], "%Y-%m-%d"))
			data_list.append(data['no_transaksi'])
			data_list.append(data['id_pengiriman__id_pengiriman'])
			if not data['id_pengiriman__id_pengiriman'] :
				data['id_pengiriman__id_pengiriman'] = '0'

			if not data['id_pengiriman__nama_pengirim'] :
				data['id_pengiriman__nama_pengirim'] = 'Tidak diketahui'

			if not data['id_pengiriman__status_pengirim'] :
				data['id_pengiriman__status_pengirim'] = 'Status Kosong'

			try :
				if data['id_pengiriman__status_pengirim'] == 'goverment':
					data_list.append(data['id_pengiriman__nama_pengirim'] + ' <span class="badge bg-warning">'+data['id_pengiriman__status_pengirim']+'</span>')
				elif data['id_pengiriman__status_pengirim'] == 'company':
					data_list.append(data['id_pengiriman__nama_pengirim'] + ' <span class="badge bg-info">'+data['id_pengiriman__status_pengirim']+'</span>')
				else:
					data_list.append(data['id_pengiriman__nama_pengirim'] + ' <span class="badge bg-success">'+data['id_pengiriman__status_pengirim']+'</span>')

				# data_list.append(data['total_tagihan'])
				if 'id_pengiriman__total_tarif' in data :
					data_list.append("Rp. {:,.2f}".format(data['id_pengiriman__total_tarif']))
				else :	
					data_list.append("Rp. {:,.2f}".format(data['total_tagihan']))
				data_list.append('<center><div class="btn-group" role="group"><a href="report?reference='+str(data['id'])+'" class="btn btn-primary btn-sm print_report==" title="Print"><i class="fa fa-fw fa-print"></i></a><a href="javascript:void(0)" data-toggle="tooltip" title="Detail Pengiriman" data-id="' + str(data['id_pengiriman_id']) + '" data-resi="' + data['id_pengiriman__id_pengiriman'] + '" class="btn btn-success btn-sm detailPengiriman"><i class="fa fa-fw fa-eye"></i></a></div></center>')
				i =  i+1
				data_pos.extend([data_list])
				
			except Exception as e:
				print(e)

		if request.is_ajax() :
			return JsonResponse({'data': data_pos}, status=200)

		return render(request, 'pos/index.html', context={'pos': data_pos, 'form': form, 'filter':_filter})

class PengirimanPOSReportView(View) :
	def get(self, request) :
		data_pos = POS.objects.all().order_by('-pk')
		data_pengiriman = {
			'nama_pengirim': '',
			'alamat_pengirim': '',
			'no_pengirim': '',
			}
		if request.GET.get('reference') :
			try :
				reference = request.GET.get('reference')
				data_pos = POS.objects.filter(id=reference)
				
				pos = list(POS.objects.filter(id=reference).values())
				pengiriman = ambil_data(get_object_or_404(Pengiriman, id=pos[0]['id_pengiriman_id']))
				data_pengiriman = {
					'nama_pengirim': pengiriman['nama_pengirim'],
					'alamat_pengirim': pengiriman['alamat_pengirim'],
					'no_pengirim': pengiriman['no_telp_pengirim'],
				}
			except Exception as e:
				print(e)
				pass
		# summary = sum(list(data_pos.values_list('total_tagihan', flat=True)))
		summary = sum(list(data_pos.values_list('id_pengiriman__total_tarif', flat=True)))
		context = {
			'data_pos': data_pos,
			'pengiriman': data_pengiriman,
			'total_all': summary,
			'tanggal_print': datetime.datetime.now()
		}
		pdf = render_to_pdf('pos/print_report.html', context)
		return HttpResponse(pdf, content_type='application/pdf')