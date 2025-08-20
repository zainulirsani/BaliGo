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

import ast

from .custom_decorator import *

class LokasiUpdate(View):
	def post(self, request):
		try:
			data_request = ast.literal_eval(request.body.decode("utf-8"))
			id_pengiriman = data_request['id_pengiriman']
			data = LogPengiriman.objects.filter(id_pengiriman=id_pengiriman).latest('created_at')

			return JsonResponse({'data': model_to_dict(data)}, status=200)
	
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)


class AssignKurir(View):
	def post(self, request):
		try:
			data_request = ast.literal_eval(request.body.decode("utf-8"))
			id_pengiriman = data_request['id_pengiriman']
			id_kurir_assign = data_request['id_kurir']

			log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=id_pengiriman)
			for log in log_pengiriman:
				log.id_kurir = id_kurir_assign
				log.save()
			return JsonResponse({'msg': 'Berhasil picking Pengiriman!', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class UpdateLocationByKurir(View):
	def post(self, request):
		try:
			data_request = ast.literal_eval(request.body.decode("utf-8"))
			id_pengiriman = data_request['id_pengiriman']
			status = data_request['status']
			titik_lokasi = data_request['titik_lokasi']
			try :
				id_kurir = data_request['id_kurir']
			except :
				id_kurir = log_old.id_kurir

			log_old = LogPengiriman.objects.filter(id_pengiriman=id_pengiriman).latest('created_at')
			log_new = LogPengiriman(
				id_pengiriman=id_pengiriman, 
				rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
				rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
				rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
				rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
				titik_lokasi = titik_lokasi,
				id_kurir = id_kurir,
				status_pengiriman = status,
				)

			if log_new.save():
				return JsonResponse({'msg': 'Berhasil Update Pengiriman!', 'type': 'success', 'data': model_to_dict(log_new)}, status=200)
			else:
				return JsonResponse({'msg': 'Gagal Update Pengiriman!', 'type': 'error'}, status=400)

		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

class KurirUpdateStatus(View):
	def post(self, request):
		try:
			id_pengiriman = int(request.POST.get('id_pengiriman', 0))
			status = request.POST.get('status')
			if str(status).lower() == 'kirim' :
				status = 'sent_by'
			else :
				status = 'arrive_at'

			titik_lokasi = request.POST.get('titik_lokasi', None)
			log_old = LogPengiriman.objects.filter(id_pengiriman=id_pengiriman).latest('created_at')

			# if log_old.status_pengiriman == 'sent_by' and log_old.id_kurir_id :
			# 	return JsonResponse({'msg': 'Data ini sudah dikonfirmasi pengiriman!', 'type': 'info'}, status=200)
			# if log_old.status_pengiriman == 'arrive_at' and log_old.id_kurir_id :
			# 	return JsonResponse({'msg': 'Data ini sudah dikonfirmasi sampai!', 'type': 'info'}, status=200)

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
			
			try :
				id_kurir = request.POST.get('id_kurir')
			except :
				id_kurir = log_old.id_kurir

			log_new = LogPengiriman(
				id_pengiriman_id=id_pengiriman, 
				rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
				rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
				rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
				rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
				titik_lokasi = titik_lokasi,
				id_kurir_id = id_kurir,
				status_pengiriman = status,
			)

			log_new.save()

			try :
				import pusher
				pusher_client = pusher.Pusher(
				  app_id='1139241',
				  key='89e810361b5ea26c0dfb',
				  secret='60ba13b071afdaa146df',
				  cluster='ap1',
				  ssl=True
				)

				pusher_client.trigger('my-channel', 'my-event', {'title':'Status Diubah','type':'success','message': 'Berhasil mengubah status pengiriman {id}'.format(id=log_new.id_pengiriman.id_pengiriman)})
			except Exception as e :
				print("Error Pusher", e)
				pass

			return JsonResponse({'msg': 'Berhasil Update Pengiriman!', 'type': 'success', 'data': model_to_dict(log_new)}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=400)

class KurirUpdateStatusQR(View):
	def post(self, request):
		try:
			id_pengiriman = request.POST.get('resi', '')
			status = request.POST.get('status_pengiriman')
			titik_lokasi = request.POST.get('titik_lokasi', None)
			pengiriman = Pengiriman.objects.get(id_pengiriman=id_pengiriman)
			log_old = LogPengiriman.objects.filter(id_pengiriman=pengiriman.id).latest('created_at')

			if log_old.status_pengiriman == 'sent_by' and log_old.id_kurir_id :
				return JsonResponse({'msg': 'Data ini sudah dikonfirmasi pengiriman!', 'type': 'info'}, status=200)

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
			
			try :
				id_kurir = request.POST.get('id_kurir')
			except :
				id_kurir = log_old.id_kurir

			log_new = LogPengiriman(
				id_pengiriman_id=pengiriman.id, 
				rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
				rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
				rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
				rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
				titik_lokasi = titik_lokasi,
				id_kurir_id = id_kurir,
				status_pengiriman = status,
			)

			log_new.save()

			try :
				import pusher
				pusher_client = pusher.Pusher(
				  app_id='1139241',
				  key='89e810361b5ea26c0dfb',
				  secret='60ba13b071afdaa146df',
				  cluster='ap1',
				  ssl=True
				)

				pusher_client.trigger('my-channel', 'my-event', {'title':'Status Diubah','type':'success','message': 'Berhasil mengubah status pengiriman {id}'.format(id=log_new.id_pengiriman.id_pengiriman)})
			except Exception as e :
				print("Error Pusher", e)
				pass

			return JsonResponse({'msg': 'Berhasil Update Pengiriman!', 'type': 'success', 'data': model_to_dict(log_new)}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=400)

class KurirUpdateStatusSampai(View):
	def post(self, request):
		try:
			id_pengiriman = request.POST.getlist('id_pengiriman[]', '')
			if id_pengiriman and len(id_pengiriman) > 0 :
				count = 0
				scan_lain_rute = 0
				belum_ada_scan_kirim = 0
				for data in id_pengiriman :
					pengiriman = Pengiriman.objects.get(id_pengiriman=data)

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

					cek_log = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id, titik_lokasi=titik_lokasi).values_list('status_pengiriman', flat=True))
					cek_pernah_scan = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id, status_pengiriman='arrive_at').values_list('id_kurir_id', flat=True))
					cek_semua_scan_lokasi = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id).order_by('created_at').values_list('titik_lokasi', flat=True))
					cek_semua_scan_status = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id).order_by('created_at').values_list('status_pengiriman', flat=True))

					if not 'done' in cek_log and request.POST.get('id_kurir') not in cek_pernah_scan :
						log_old = LogPengiriman.objects.filter(id_pengiriman=pengiriman.id).latest('created_at')
						try :
							id_kurir = request.POST.get('id_kurir')
						except :
							id_kurir = log_old.id_kurir
						if 'arrive_at' not in cek_log and 'sent_by' not in cek_log :
							outlet_pengiriman = pengiriman.outlet_pengiriman.titik_lokasi if pengiriman.outlet_pengiriman else 0
							outlet_penerimaan = pengiriman.outlet_penerimaan.titik_lokasi if pengiriman.outlet_penerimaan else 0
							gudang_penerimaan = pengiriman.gudang_penerimaan.titik_lokasi if pengiriman.gudang_penerimaan else 0
							gudang_pengiriman = pengiriman.gudang_pengiriman.titik_lokasi if pengiriman.gudang_pengiriman else 0
							data_lokasi_scan = [outlet_pengiriman, gudang_pengiriman, gudang_penerimaan, outlet_penerimaan]

							if titik_lokasi in data_lokasi_scan :
								if titik_lokasi == outlet_pengiriman :
									count += 1
									log_new = LogPengiriman(
										id_pengiriman_id=pengiriman.id, 
										rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
										rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
										rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
										rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
										titik_lokasi = titik_lokasi,
										id_kurir_id = id_kurir,
										status_pengiriman = 'arrive_at',
									)

									log_new.save()

									try :
										import pusher
										pusher_client = pusher.Pusher(
										app_id='1139241',
										key='89e810361b5ea26c0dfb',
										secret='60ba13b071afdaa146df',
										cluster='ap1',
										ssl=True
										)

										pusher_client.trigger('my-channel', 'my-event', {'title':'Status Diubah','type':'success','message': 'Berhasil mengubah status sampai {id}'.format(id=log_new.id_pengiriman.id_pengiriman)})
									except Exception as e :
										print("Error Pusher", e)
										pass
								else :
									if log_old.status_pengiriman == 'sent_by' :
										try :
											cek_urutan_scan_saat_ini = data_lokasi_scan.index(titik_lokasi)
										except :
											cek_urutan_scan_saat_ini = None
										try :
											cek_urutan_scan_terakhir = data_lokasi_scan.index(log_old.titik_lokasi)
										except :
											cek_urutan_scan_terakhir = None
										if not cek_urutan_scan_saat_ini == None and not cek_urutan_scan_terakhir == None and cek_urutan_scan_saat_ini >= cek_urutan_scan_terakhir :
											count += 1
											log_new = LogPengiriman(
												id_pengiriman_id=pengiriman.id, 
												rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
												rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
												rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
												rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
												titik_lokasi = titik_lokasi,
												id_kurir_id = id_kurir,
												status_pengiriman = 'arrive_at',
											)

											log_new.save()

											try :
												import pusher
												pusher_client = pusher.Pusher(
												app_id='1139241',
												key='89e810361b5ea26c0dfb',
												secret='60ba13b071afdaa146df',
												cluster='ap1',
												ssl=True
												)

												pusher_client.trigger('my-channel', 'my-event', {'title':'Status Diubah','type':'success','message': 'Berhasil mengubah status sampai {id}'.format(id=log_new.id_pengiriman.id_pengiriman)})
											except Exception as e :
												print("Error Pusher", e)
												pass
										else :
											return JsonResponse({'msg': 'Tidak dapat melakukan scan sampai karena urutan scan sudah didahului outlet / gudang selanjutnya', 'type': 'warning'}, status=412)
									else :
										belum_ada_scan_kirim += 1
							else :
								scan_lain_rute += 1

				if count > 0 and count < len(id_pengiriman) :
					return JsonResponse({'msg': 'Berhasil Update Pengiriman, pengiriman dengan status tanda terima ataupun sudah pernah scan sampai sebelumnya tidak akan di update', 'type': 'success'}, status=200)
				elif count > 0 and count == len(id_pengiriman) :
					return JsonResponse({'msg': 'Berhasil Update Pengiriman', 'type': 'success'}, status=200)
				else :
					if 'done' in cek_log :
						return JsonResponse({'msg': 'Pengiriman sudah di tanda terima sebelumnya, tidak dapat mengupdate data', 'type': 'warning'}, status=412)
					elif scan_lain_rute > 0 :
						return JsonResponse({'msg': 'Tidak dapat memproses scan karena gudang / outlet tidak termasuk dalam rute', 'type': 'warning'}, status=412)
					elif belum_ada_scan_kirim > 0 :
						return JsonResponse({'msg': 'Belum ada scan kirim dari rute sebelumnya, tidak dapat melanjutkan scan', 'type': 'warning'}, status=412)
					else :
						return JsonResponse({'msg': 'Pengiriman sudah pernah di scan pada outlet / gudang ini sebelumnya, tidak dapat mengupdate', 'type': 'warning'}, status=412)

			return JsonResponse({'msg': 'Tidak ada data yang dikirim', 'type': 'warning'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=400)

class KurirUpdateStatusKirim(View):
	def post(self, request):
		try:
			id_pengiriman = request.POST.getlist('id_pengiriman[]', '')
			if id_pengiriman and len(id_pengiriman) > 0 :
				count = 0
				scan_lain_rute = 0
				belum_ada_scan_kirim = 0
				for data in id_pengiriman :
					pengiriman = Pengiriman.objects.get(id_pengiriman=data)
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

					cek_log = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id, titik_lokasi=titik_lokasi).values_list('status_pengiriman', flat=True))
					cek_pernah_scan = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id, status_pengiriman='sent_by').values_list('id_kurir_id', flat=True))
					cek_semua_scan_lokasi = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id).order_by('created_at').values_list('titik_lokasi', flat=True))
					cek_semua_scan_status = list(LogPengiriman.objects.filter(id_pengiriman=pengiriman.id).order_by('created_at').values_list('status_pengiriman', flat=True))
					if not 'done' in cek_log and request.POST.get('id_kurir') not in cek_pernah_scan :
						log_old = LogPengiriman.objects.filter(id_pengiriman=pengiriman.id).latest('created_at')						
						try :
							id_kurir = request.POST.get('id_kurir')
						except :
							id_kurir = log_old.id_kurir
							
						if 'sent_by' not in cek_log or 'sent_by' not in cek_log and 'arrive_at' in cek_log :
							outlet_pengiriman = pengiriman.outlet_pengiriman.titik_lokasi if pengiriman.outlet_pengiriman else 0
							outlet_penerimaan = pengiriman.outlet_penerimaan.titik_lokasi if pengiriman.outlet_penerimaan else 0
							gudang_penerimaan = pengiriman.gudang_penerimaan.titik_lokasi if pengiriman.gudang_penerimaan else 0
							gudang_pengiriman = pengiriman.gudang_pengiriman.titik_lokasi if pengiriman.gudang_pengiriman else 0
							data_lokasi_scan = [outlet_pengiriman, gudang_pengiriman, gudang_penerimaan, outlet_penerimaan]

							if titik_lokasi in data_lokasi_scan :
								if titik_lokasi == outlet_pengiriman :
									count += 1
									log_new = LogPengiriman(
										id_pengiriman_id=pengiriman.id, 
										rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
										rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
										rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
										rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
										titik_lokasi = titik_lokasi,
										id_kurir_id = id_kurir,
										status_pengiriman = 'sent_by',
									)

									log_new.save()

									try :
										import pusher
										pusher_client = pusher.Pusher(
										app_id='1139241',
										key='89e810361b5ea26c0dfb',
										secret='60ba13b071afdaa146df',
										cluster='ap1',
										ssl=True
										)

										pusher_client.trigger('my-channel', 'my-event', {'title':'Status Diubah','type':'success','message': 'Berhasil mengubah status kirim {id}'.format(id=log_new.id_pengiriman.id_pengiriman)})
									except Exception as e :
										print("Error Pusher", e)
										pass
								else :
									if log_old.status_pengiriman == 'arrive_at' and titik_lokasi == log_old.titik_lokasi or log_old.status_pengiriman == 'sent_by' :
										try :
											cek_urutan_scan_saat_ini = data_lokasi_scan.index(titik_lokasi)
										except :
											cek_urutan_scan_saat_ini = None
										try :
											cek_urutan_scan_terakhir = data_lokasi_scan.index(log_old.titik_lokasi)
										except :
											cek_urutan_scan_terakhir = None
										if not cek_urutan_scan_saat_ini == None and not cek_urutan_scan_terakhir == None and cek_urutan_scan_saat_ini >= cek_urutan_scan_terakhir :
											count += 1
											log_new = LogPengiriman(
												id_pengiriman_id=pengiriman.id, 
												rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
												rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
												rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
												rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
												titik_lokasi = titik_lokasi,
												id_kurir_id = id_kurir,
												status_pengiriman = 'sent_by',
											)

											log_new.save()

											try :
												import pusher
												pusher_client = pusher.Pusher(
												app_id='1139241',
												key='89e810361b5ea26c0dfb',
												secret='60ba13b071afdaa146df',
												cluster='ap1',
												ssl=True
												)

												pusher_client.trigger('my-channel', 'my-event', {'title':'Status Diubah','type':'success','message': 'Berhasil mengubah status kirim {id}'.format(id=log_new.id_pengiriman.id_pengiriman)})
											except Exception as e :
												print("Error Pusher", e)
												pass
										else :
											return JsonResponse({'msg': 'Tidak dapat melakukan scan kirim karena urutan scan sudah didahului outlet / gudang selanjutnya', 'type': 'warning'}, status=412)
									else :
										belum_ada_scan_kirim += 1

							else :
								scan_lain_rute += 1

				if count > 0 and count < len(id_pengiriman) :
					return JsonResponse({'msg': 'Berhasil Update Pengiriman, pengiriman dengan status tanda terima ataupun sudah pernah scan kirim sebelumnya tidak akan di update', 'type': 'success'}, status=200)
				elif count > 0 and count == len(id_pengiriman) :
					return JsonResponse({'msg': 'Berhasil Update Pengiriman', 'type': 'success'}, status=200)
				else :
					if 'done' in cek_log :
						return JsonResponse({'msg': 'Pengiriman sudah di tanda terima sebelumnya, tidak dapat mengupdate data', 'type': 'warning'}, status=412)
					elif scan_lain_rute > 0 :
						return JsonResponse({'msg': 'Tidak dapat memproses scan karena gudang / outlet tidak termasuk dalam rute', 'type': 'warning'}, status=412)
					elif belum_ada_scan_kirim > 0 :
						return JsonResponse({'msg': 'Belum ada scan kirim dari rute sebelumnya, tidak dapat melanjutkan scan', 'type': 'warning'}, status=412)
					else :
						return JsonResponse({'msg': 'Pengiriman sudah pernah di scan pada outlet / gudang ini sebelumnya, tidak dapat mengupdate', 'type': 'warning'}, status=412)

			return JsonResponse({'msg': 'Tidak ada data yang dikirim', 'type': 'warning'}, status=200)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=400)

class KurirUpdateLokasiTerkini(View):
	def post(self, request):
		try:
			kurir = User.objects.filter(pk=request.POST.get('id_kurir', 0)) 
			if(kurir.exists()) :
				if(hasattr(kurir.first(), 'penempatan_toko')) :
					outlet_penerimaan = kurir.first().penempatan_toko.id
					titik_lokasi_toko = kurir.first().penempatan_toko.titik_lokasi
					pengiriman = list(Pengiriman.objects.filter(outlet_penerimaan_id=outlet_penerimaan).values_list('id', flat=True))
					if(len(pengiriman)) :
						titik_lokasi = str(request.POST.get('latitude', '0')) + ', ' + str(request.POST.get('longitude', '0'))
						for data in pengiriman :
							try :
								cek_log = list(LogPengiriman.objects.filter(id_pengiriman=dataG).values_list('status_pengiriman', flat=True))
								if not 'done' in cek_log :
									log_old = LogPengiriman.objects.filter(id_pengiriman=data).latest('created_at')
									if(log_old) :
										print('LOG OLD', log_old.status_pengiriman)
										if(log_old.status_pengiriman == 'sent_by' and log_old.titik_lokasi == titik_lokasi_toko or log_old.status_pengiriman == 'arrive_at' and log_old.titik_lokasi == titik_lokasi_toko) :
											log_new = LogPengiriman(
												id_pengiriman_id=data, 
												rute_pengiriman_outlet=log_old.rute_pengiriman_outlet, 
												rute_pengiriman_gudang=log_old.rute_pengiriman_gudang, 
												rute_pengiriman_gudang_akhir= log_old.rute_pengiriman_gudang_akhir,
												rute_pengiriman_outlet_akhir = log_old.rute_pengiriman_outlet_akhir,
												titik_lokasi = titik_lokasi,
												id_kurir_id = kurir.first().id,
												status_pengiriman = 'sent_by',
											)
											log_new.save()
							except :
								# Pass jika resi tidak ditemukan
								pass
						return JsonResponse({'msg': 'Berhasil update lokasi untuk semua resi!', 'type': 'success'}, status=200)
			return JsonResponse({'msg': 'Gagal mengupdate lokasi, silahkan coba beberapa saat lagi', 'type': 'error'}, status=500)
		except Exception as e:
			return JsonResponse({'msg': 'Terjadi Kesalahan, {}'.format(e), 'type': 'error'}, status=400)

