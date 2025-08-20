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

from ekspedisi.views.pengiriman_ambil_data import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

@method_decorator(login_required(login_url='/mobile_kurir'), name='get')
class KurirPengirimanView(View):
	def get(self, request):
		pengiriman = []
		log_pengiriman = []
		try :
			outlet = int(getattr(request.user.penempatan_toko,'id', 0))
			gudang = int(getattr(request.user.penempatan_gudang, 'id', 0))
			try :
				log_pengiriman = LogPengiriman.objects.filter(id_kurir_id=request.user.id).order_by('created_at')
			except Exception as e:
				print(e)
				pass

			if outlet :
				pengiriman = list(Pengiriman.objects.filter(is_active=True, outlet_pengiriman_id=outlet))
			else :
				pengiriman = list(Pengiriman.objects.filter(is_active=True))
		except Exception as e:
			print(e)
			pass
		return render(request, 'mobile_kurir/templates/pengiriman/index.html', context={
			'pengiriman': pengiriman,
			'log_pengiriman': log_pengiriman,
			'is_active_pengiriman':'active'
		})

	@csrf_exempt
	def post(self, request):
		try : 
			form = PengirimanForm(request.POST)
			formPelacakan = LogPengirimanForm()
			if form.is_valid():
				try:
					new_pengiriman = form.save(commit=False)
					new_pengiriman.id_pengiriman = generate_id('ER', 8)
					new_pengiriman.save()
					# print(new_pengiriman)
					new_pelacakan = formPelacakan.save(commit=False)
					new_pelacakan.id_pengiriman = get_object_or_404(Pengiriman, id_pengiriman=new_pengiriman)
					new_pelacakan.rute_pengiriman_outlet = get_object_or_404(Toko, id=request.POST['outlet_pengiriman'])
					new_pelacakan.rute_pengiriman_outlet_akhir = get_object_or_404(Toko, id=request.POST['outlet_penerimaan'])
					new_pelacakan.rute_pengiriman_gudang = get_object_or_404(Gudang, id=request.POST['rute_pengiriman_gudang'])
					new_pelacakan.rute_pengiriman_gudang_akhir = get_object_or_404(Gudang, id=request.POST['rute_pengiriman_gudang_akhir'])
					new_pelacakan.status_pengiriman = 'waiting'
					new_pelacakan.save()

					return JsonResponse({'msg': 'Berhasil Menambah data pengiriman', 'type': 'success'}, status=200)
				except Exception as e :
					return JsonResponse({'msg': 'Gagal Menambah data pengiriman {}'.format(e), 'type': 'error'}, status=400)
			else:
				error = [er[0] for er in form.errors.values()]
				print(form.errors)
				error = "<br> ".join(error)
				return JsonResponse({'msg': 'Gagal, Form pengiriman Tidak Valid <br> {}'.format(error), 'type': 'error'}, status=422)
		except Exception as e :
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class KurirPengirimanArsip(View):
	def post(self, request, id):
		pengiriman = Pengiriman.objects.get(id=id)
		log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id) # => banyak log Pengiriman
		status = LogPengiriman.objects.filter(id_pengiriman=id).latest('created_at')
		if status.status_pengiriman == 'done':
			try:
				pengiriman.is_active = False
				pengiriman.save()
				for log in log_pengiriman:
					log.is_active = False
					log.save()
				return JsonResponse({'msg': 'Berhasil Menghapus Data pengiriman (Arsip)', 'type': 'success'}, status=200)
			except:
				return JsonResponse({'msg': 'Gagal Mengapus Data pengiriman (Arsip)', 'type': 'error'}, status=400)
		else:
			return JsonResponse({'msg': 'Tidak Bisa Arsip!, Status Pengiriman belum Selesai', 'type': 'error'}, status=400)


class KurirPengirimanDetailView(View):
	def get(self, request, id):
		try:
			try :
				id = Pengiriman.objects.get(id=id)
				id = id.pk
			except Exception as e:
				id = Pengiriman.objects.get(id_pengiriman=id)
				id = id.pk

			pengiriman = ambil_data(get_object_or_404(Pengiriman, id=id))
			rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).order_by('-pk').first()
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).values()

			if rute_pengiriman.id_kurir:
				kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=rute_pengiriman.id_kurir.id))
			else:
				kurir_pengiriman = ambil_kurir('')
			rute = ambil_rute(rute_pengiriman)
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).order_by('created_at')[0])
			return render(request, 'mobile_kurir/templates/pengiriman/detail_kirim.html', context={
				'data':pengiriman,
				'rute':rute,
				'kurir': kurir_pengiriman,
				'status':status_pengiriman,
				'log':list(log_pengiriman),
				'is_active_pengiriman':'active'
			})
		except Exception as e:
			storage = messages.get_messages(request)
			storage.used = True
			pesan = str(e)
			messages.warning(request, pesan)
			return redirect('kurir_pengiriman')

	def post(self, request, id):
		try: 
			obj = get_object_or_404(Pengiriman, id=id)
		except Exception as e :
			print(e)

class KurirPengirimanDetailViewReadOnly(View):
	def get(self, request, id):
		try:
			try :
				id = Pengiriman.objects.get(id=id)
				id = id.pk
			except Exception as e:
				id = Pengiriman.objects.get(id_pengiriman=id)
				id = id.pk

			pengiriman = ambil_data(get_object_or_404(Pengiriman, id=id))
			rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).order_by('-pk').first()
			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id).values()

			if rute_pengiriman.id_kurir:
				kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=rute_pengiriman.id_kurir.id))
			else:
				kurir_pengiriman = ambil_kurir('')
			rute = ambil_rute(rute_pengiriman)
			status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=id).order_by('created_at')[0])
			return render(request, 'mobile_kurir/templates/pengiriman/detail_kirim_view.html', context={
				'data':pengiriman,
				'rute':rute,
				'kurir': kurir_pengiriman,
				'status':status_pengiriman,
				'log':list(log_pengiriman),
				'is_active_pengiriman':'active'
			})
		except Exception as e:
			storage = messages.get_messages(request)
			storage.used = True
			pesan = str(e)
			messages.warning(request, pesan)
			return redirect('kurir_dashboard')

class KurirUpdateStatusTTD(View) :
	def post(self, request) :
		try :
			resi = request.POST.get('resi', 0)
			pengiriman_check = Pengiriman.objects.filter(id_pengiriman=resi)
			if pengiriman_check.exists() :
				id_pengiriman = pengiriman_check.first().id
				cek_log = list(LogPengiriman.objects.filter(id_pengiriman=id_pengiriman).values_list('status_pengiriman', flat=True))
				if not 'done' in cek_log :
					log_terakhir = pengiriman_check.first().log_pengiriman.filter(id_pengiriman=id_pengiriman).order_by('-pk')
					if log_terakhir.exists() and str(log_terakhir.first().status_pengiriman).lower() == 'done' :
						return JsonResponse({'msg':'Resi sudah berhasil di tanda terima', 'type':'warning'})
					
					if len(request.FILES.getlist('foto')) < 3 :
						return JsonResponse({'msg':'Upload minimal 3 bukti foto', 'type':'warning'})

					if log_terakhir.exists() and str(log_terakhir.first().status_pengiriman).lower() == 'sent_by' :
						titik_lokasi = None
						if not titik_lokasi :
							try :
								if request.user.penempatan_gudang :
									titik_lokasi = request.user.penempatan_gudang.titik_lokasi
								elif request.user.penempatan_toko:
									titik_lokasi = request.user.penempatan_toko.titik_lokasi
								else :
									raise Exception('Tidak dapat menentukan kepemilikan Gudang atau Toko, cek kembali ID anda')
							except Exception as e:
								raise Exception(str(e))


						outlet_pengiriman = pengiriman_check.first().outlet_pengiriman.titik_lokasi if pengiriman_check.first().outlet_pengiriman else 0
						outlet_penerimaan = pengiriman_check.first().outlet_penerimaan.titik_lokasi if pengiriman_check.first().outlet_penerimaan else 0
						gudang_penerimaan = pengiriman_check.first().gudang_penerimaan.titik_lokasi if pengiriman_check.first().gudang_penerimaan else 0
						gudang_pengiriman = pengiriman_check.first().gudang_pengiriman.titik_lokasi if pengiriman_check.first().gudang_pengiriman else 0
						data_lokasi_scan = [outlet_pengiriman, outlet_penerimaan, gudang_pengiriman, gudang_penerimaan]

						if titik_lokasi in data_lokasi_scan :
							
							nama_penerima = request.POST.get('nama_penerima', 'Yang Bersangkutan')
							data_to_send = {'id_pengiriman': id_pengiriman, 'nama_penerima': nama_penerima, 'keterangan': 'Paket sudah diterima'}
							form_ttd = KurirTTD(data=data_to_send)
							if form_ttd.is_valid() :
								ttd = form_ttd.save()
								data_bukti_ttd = {'id_ttd': ttd.id}

								if request.FILES.getlist('foto') :
									for f in request.FILES.getlist('foto'):
										photo_size = f.size if hasattr(f, 'size') else 0;
										if photo_size and photo_size > 5242880 :
											raise Exception('Foto yang diupload tidak boleh lebih dari 5Mb per Foto')
										bukti_ttd = KurirTTDBuktiFoto(data_bukti_ttd, request.FILES)
										if bukti_ttd.is_valid() :
											bukti = bukti_ttd.save(commit=False)
											bukti.foto = f
											bukti.save()
									
								# pengiriman_check.update(is_active=0)
								formPelacakan = LogPengirimanForm()
								new_pelacakan = formPelacakan.save(commit=False)
								new_pelacakan.id_pengiriman_id = id_pengiriman
								new_pelacakan.id_kurir_id = request.user.id
								new_pelacakan.rute_pengiriman_outlet = pengiriman_check.first().outlet_pengiriman
								new_pelacakan.rute_pengiriman_outlet_akhir = pengiriman_check.first().outlet_penerimaan
								new_pelacakan.rute_pengiriman_gudang = pengiriman_check.first().gudang_pengiriman
								new_pelacakan.rute_pengiriman_gudang_akhir = pengiriman_check.first().gudang_penerimaan
								new_pelacakan.titik_lokasi = pengiriman_check.first().outlet_penerimaan.titik_lokasi
								new_pelacakan.status_pengiriman = 'done'
								new_pelacakan.save()

								return JsonResponse({'msg':'Berhasil Mengupload Tanda Terima', 'type':'success'})
							else :
								print(form_ttd.errors)
								return JsonResponse({'msg': 'Gagal memproses tanda terima, coba beberapa saat lagi', 'type':'error', 'error':form_ttd.errors.as_json()})
						else :
							return JsonResponse({'msg': 'Tidak dapat melakukan tanda terima karena outlet tidak sesuai rute pengiriman', 'type': 'error'}, status=400)

					else :
						return JsonResponse({'msg': 'Tidak ada scan kirim dari outlet / gudang sebelumnya, tidak dapat melakaukan tanda terima', 'type': 'error'}, status=400)

				return JsonResponse({'msg':'Resi sudah berhasil di tanda terima sebelumnya', 'type':'warning'})
			else :
				return JsonResponse({'msg': 'Resi tidak ditemukan, pastikan memasukkan resi yang valid', 'type': 'error'}, status=400)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=400)
