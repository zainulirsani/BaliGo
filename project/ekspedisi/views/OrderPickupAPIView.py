from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from rest_framework.views import APIView

import datetime
import numpy as np
import math
from random import randint

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from ..models import *
from ..forms import *
from .PengirimanAPIView import *

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.utils.timezone import get_current_timezone, make_aware, now
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.conf import settings as CONF
import requests as req_api

from django.urls import reverse

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class GetLocationDetail(APIView) :
	def post(self, request) :
		result = {
			'data': {},
			'msg': '',
			'status': 200,
		}

		try :
			URL_GEO = 'https://api.openrouteservice.org/geocode/search?'
			API_GEO = CONF.API_OPEN_ROUTE_SERVICE

			# username = request.POST.get('username')
			# password = request.POST.get('password')

			# user = authenticate(username=username, password=password)
			# if user:
			kode_pos_pengirim = request.POST.get('kode_pos_pengirim')
			kode_pos_penerima = request.POST.get('kode_pos_penerima')
			pengemasan = request.POST.get('pengemasan')
			berat = request.POST.get('berat')
			extra_tarif = request.POST.get('extra_tarif', False)
			if not berat :
				raise Exception('Berat tidak boleh kosong, karena berpengaruh pada kalkulasi harga')
			else :
				berat_ons_order = int(str("{:.1f}".format(float(berat))[-1:]))
				if berat_ons_order >= 1 :
					berat = math.floor(float(str("{:.1f}".format(float(berat))))) + 1 
				else :
					berat = math.floor(float(str("{:.1f}".format(float(berat)))))
				print("BERAT YANG DIBEBANKAN", berat)


			try:
				data_pengirim = KodePos.objects.filter(kode_pos = kode_pos_pengirim).first()
				data_penerima = KodePos.objects.filter(kode_pos = kode_pos_penerima).first()
				if not data_pengirim and not data_penerima :
					raise Exception('Tidak dapat menemukan kode pos penerima ataupun pengirim')
				elif not data_pengirim : 
					raise Exception('Tidak dapat menemukan kode pos pengirim')
				elif not data_penerima :
					raise Exception('Tidak dapat menemukan kode pos penerima')

				provinsi_penerima = data_penerima.provinsi_id.id
				kota_penerima = data_penerima.kota_id.id
				kecamatan_penerima = data_penerima.kecamatan_id.id
				desa_penerima = data_penerima.desa_id.id

				nama_provinsi_penerima = data_penerima.provinsi_id.nama_provinsi
				nama_kota_penerima = data_penerima.kota_id.nama_kota
				nama_kecamatan_penerima = data_penerima.kecamatan_id.nama_kecamatan
				nama_desa_penerima = data_penerima.desa_id.nama_desa

				provinsi_pengirim = data_pengirim.provinsi_id.id
				kota_pengirim = data_pengirim.kota_id.id
				kecamatan_pengirim = data_pengirim.kecamatan_id.id
				desa_pengirim = data_pengirim.desa_id.id

				nama_provinsi_pengirim = data_pengirim.provinsi_id.nama_provinsi
				nama_kota_pengirim = data_pengirim.kota_id.nama_kota
				nama_kecamatan_pengirim = data_pengirim.kecamatan_id.nama_kecamatan
				nama_desa_pengirim = data_pengirim.desa_id.nama_desa

				result['data']['data_pengirim'] = {
					'kode_pos' : data_pengirim.kode_pos,
					'desa' : nama_desa_pengirim,
					'kecamatan' : nama_kecamatan_pengirim,
					'kota' : nama_kota_pengirim,
					'provinsi' : nama_provinsi_pengirim
				}
				result['data']['data_penerima'] = {
					'kode_pos' : data_penerima.kode_pos,
					'desa' : nama_desa_penerima,
					'kecamatan' : nama_kecamatan_penerima,
					'kota' : nama_kota_penerima,
					'provinsi' : nama_provinsi_penerima
				}

				try :
					arr_penerima = [nama_desa_penerima,nama_kecamatan_penerima,nama_kota_penerima,nama_provinsi_penerima]
					arr_pengirim = [nama_desa_pengirim,nama_kecamatan_pengirim,nama_kota_pengirim,nama_provinsi_pengirim]					
					coordinat_penerima, extra_cash_penerima, provinsi_terima = get_location(arr_alamat=arr_penerima, URL_GEO=URL_GEO, API_GEO=API_GEO)
					coordinat_pengirim, extra_cash_pengirim, provinsi_kirim = get_location(arr_alamat=arr_pengirim, URL_GEO=URL_GEO, API_GEO=API_GEO)
					data_extra_tarif_penerima = get_extra_tarif(extra_cash_penerima)

					result['data']['extra_cash_pengirim'] = extra_cash_pengirim
					result['data']['extra_cash_penerima'] = extra_cash_penerima
					result['data']['koordinat_penerima'] = coordinat_penerima
					result['data']['koordinat_pengirim'] = coordinat_pengirim

					# cek outlet pengirim terdekat
					uri_toko_1 = str(request.build_absolute_uri('/admin/toko/')) + str(coordinat_pengirim[1]) + '/' + str(coordinat_pengirim[0]) + '/'
					PARAMS = {}
					outlet_pengirim = req_api.get(url = uri_toko_1, params = PARAMS)
					outlet_pengirim = outlet_pengirim.json()
					result['data']['outlet_pengirim'] = outlet_pengirim
					outlet_pengirim_titik_lokasi = outlet_pengirim['data']['titik_lokasi'].split(',')

					# cek gudang pengirim terdekat
					uri_gudang_1 = str(request.build_absolute_uri('/admin/gudang/')) + str(outlet_pengirim_titik_lokasi[0]) + '/' + str(outlet_pengirim_titik_lokasi[1]) + '/'
					PARAMS = {}
					gudang_pengirim = req_api.get(url = uri_gudang_1, params = PARAMS)
					gudang_pengirim = gudang_pengirim.json()
					result['data']['gudang_pengirim'] = gudang_pengirim
					gudang_pengirim_titik_lokasi = gudang_pengirim['data']['titik_lokasi'].split(',')

					# cek outlet penerima terdekat
					uri_toko_2 = str(request.build_absolute_uri('/admin/toko/nearest/')) + str(coordinat_penerima[1]) + '/' + str(coordinat_penerima[0]) + '/'
					PARAMS = {}
					outlet_penerima = req_api.get(url = uri_toko_2, params = PARAMS)
					outlet_penerima = outlet_penerima.json()
					result['data']['outlet_penerima'] = outlet_penerima
					outlet_penerima_titik_lokasi = outlet_penerima['data']['titik_lokasi'].split(',')

					# cek gudang penerima terdekat
					uri_gudang_2 = str(request.build_absolute_uri('/admin/gudang/')) + str(outlet_penerima_titik_lokasi[0]) + '/' + str(outlet_penerima_titik_lokasi[1]) + '/'
					PARAMS = {}
					gudang_penerima = req_api.get(url = uri_gudang_2, params = PARAMS)
					gudang_penerima = gudang_penerima.json()
					result['data']['gudang_penerima'] = gudang_penerima
					gudang_penerima_titik_lokasi = gudang_penerima['data']['titik_lokasi'].split(',')

					try :
						outlet1_gudang1 = get_location_new(outlet_pengirim_titik_lokasi, gudang_pengirim_titik_lokasi)
						gudang1_gudang2 = get_location_new(gudang_pengirim_titik_lokasi, gudang_penerima_titik_lokasi)
						gudang2_outlet2 = get_location_new(gudang_penerima_titik_lokasi, outlet_penerima_titik_lokasi)
						outlet2_penerima = get_location_new(outlet_penerima_titik_lokasi, coordinat_penerima, True)
					except :
						try :
							outlet1_gudang1 = hitung_jarak(outlet_pengirim_titik_lokasi, gudang_pengirim_titik_lokasi)
							gudang1_gudang2 = hitung_jarak(gudang_pengirim_titik_lokasi, gudang_penerima_titik_lokasi)
							gudang2_outlet2 = hitung_jarak(gudang_penerima_titik_lokasi, outlet_penerima_titik_lokasi)
							outlet2_penerima = hitung_jarak(outlet_penerima_titik_lokasi, coordinat_penerima, True)
						except :
							outlet1_gudang1 = 0
							gudang1_gudang2 = 0
							gudang2_outlet2 = 0
							outlet2_penerima = 0

					jarak_total = (float(outlet1_gudang1) + float(gudang1_gudang2) + float(gudang2_outlet2) + float(outlet2_penerima)) / 1000

					data_pengemasan = get_harga_pengemasan(pengemasan)
					nama_pengemasan = data_pengemasan['nama_pengemasan']
					tarif_pengemasan = data_pengemasan['harga']
					tarif_kilometer = get_harga_kilometer_new(jarak_total)
					tarif_berat = get_harga_berat_new(berat)
					tarif_gudang = get_harga_gudang(gudang_pengirim['data']['id'],gudang_penerima['data']['id'])
					# tarif_extra_pengirim = data_extra_tarif_pengirim['harga']
					if extra_tarif:
						tarif_extra_penerima = data_extra_tarif_penerima['harga']
					else:
						tarif_extra_penerima = 0

					final_result = get_list_layanan(tarif_berat, tarif_kilometer, tarif_gudang, tarif_pengemasan, tarif_extra_penerima)

					# result['data'] = {'lokasi_outlet_1': list(lokasi_outlet_1), 'coordinat_penerima': list(coordinat_penerima)}
					result['total_tarif_layanan'] = final_result['data']
					result['berat_input'] = {
						'berat': request.POST.get('berat',0), 
						'satuan': 'Kg'
					}
					result['pengemasan'] = nama_pengemasan
					result['tarif_berat'] = tarif_berat
					result['tarif_kilometer'] = tarif_kilometer
					result['tarif_gudang'] = tarif_gudang
					result['tarif_pengemasan'] = tarif_pengemasan
					result['extra_tarif_penerima'] = tarif_extra_penerima

				except Exception as e: 
					raise Exception("Gagal memperoleh koordinat penerima dan pengirim, {}".format(str(e)))

			except Exception as e:
				result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
				result['status'] = 422
			
			return JsonResponse({'result': result}, status=result['status'])
		except Exception as e:
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 400
			return JsonResponse({'result': result}, status=result['status'])

class OrderPickupPelangganAPI(APIView):
	def post(self, request):
		# Under construction
		result = {
			'data': [],
			'msg': '',
			'status': 200,
		}

		try :
			URL_GEO = 'https://api.openrouteservice.org/geocode/search?'
			API_GEO = CONF.API_OPEN_ROUTE_SERVICE

			# username = request.POST.get('username')
			# password = request.POST.get('password')

			# user = authenticate(username=username, password=password)
			# if user:
			kode_pos_pengirim = request.POST.get('kode_pos_pengirim')
			kode_pos_penerima = request.POST.get('kode_pos_penerima')
			berat = request.POST.get('berat',0)
			try:
				data_pengirim = KodePos.objects.filter(kode_pos = kode_pos_pengirim).first()
				data_penerima = KodePos.objects.filter(kode_pos = kode_pos_penerima).first()
				if not data_pengirim and not data_penerima :
					raise Exception('Tidak dapat menemukan kode pos penerima ataupun pengirim')
				elif not data_pengirim : 
					raise Exception('Tidak dapat menemukan kode pos pengirim')
				elif not data_penerima :
					raise Exception('Tidak dapat menemukan kode pos penerima')

				if not berat :
					raise Exception('Berat tidak boleh kosong, karena berpengaruh pada kalkulasi harga')

				provinsi_penerima = data_penerima.provinsi_id.id
				kota_penerima = data_penerima.kota_id.id
				kecamatan_penerima = data_penerima.kecamatan_id.id
				desa_penerima = data_penerima.desa_id.id

				nama_provinsi_penerima = data_penerima.provinsi_id.nama_provinsi
				nama_kota_penerima = data_penerima.kota_id.nama_kota
				nama_kecamatan_penerima = data_penerima.kecamatan_id.nama_kecamatan
				nama_desa_penerima = data_penerima.desa_id.nama_desa

				provinsi_pengirim = data_pengirim.provinsi_id.id
				kota_pengirim = data_pengirim.kota_id.id
				kecamatan_pengirim = data_pengirim.kecamatan_id.id
				desa_pengirim = data_pengirim.desa_id.id

				nama_provinsi_pengirim = data_pengirim.provinsi_id.nama_provinsi
				nama_kota_pengirim = data_pengirim.kota_id.nama_kota
				nama_kecamatan_pengirim = data_pengirim.kecamatan_id.nama_kecamatan
				nama_desa_pengirim = data_pengirim.desa_id.nama_desa

				alamat_pengirim = request.POST.get('alamat_pengirim')
				if not alamat_pengirim :
					raise Exception('Alamat Pengirim tidak boleh kosong')
				alamat_penerima = request.POST.get('alamat_penerima')
				if not alamat_penerima :
					raise Exception('Alamat Penerima tidak boleh kosong')
				nama_pengirim = request.POST.get('nama_pengirim')
				if not nama_pengirim :
					raise Exception('Nama Pengirim tidak boleh kosong')
				nama_penerima = request.POST.get('nama_penerima')
				if not nama_penerima :
					raise Exception('Nama Penerima tidak boleh kosong')
				# status_pengirim = request.POST.get('status_pengirim')
				no_telp_pengirim = request.POST.get('no_telp_pengirim')
				if not no_telp_pengirim :
					raise Exception('No Telp Pengirim tidak boleh kosong')
				no_telp_penerima = request.POST.get('no_telp_penerima')

				jenis_barang = request.POST.get('jenis_barang')
				detail_barang = request.POST.get('detail_barang')
				pengemasan = request.POST.get('pengemasan') #id pengemasan
				layanan = request.POST.get('layanan') #id layanan
				# berat = request.POST.get('berat') if request.POST.get('berat') else '0'
				print('INI ADALAH DATA ORDER', str("{:.1f}".format(float(request.POST.get('berat', 0)))))
				berat_ons_order = int(str("{:.1f}".format(float(request.POST.get('berat',0)))[-1:]))
				if berat_ons_order >= 1 :
					berat = math.floor(float(str("{:.1f}".format(float(request.POST.get('berat',0)))))) + 1 
				else :
					berat = math.floor(float(str("{:.1f}".format(float(request.POST.get('berat',0))))))
				print("BERAT YANG DIBEBANKAN", berat)
				jumlah = request.POST.get('jumlah')
				satuan = request.POST.get('satuan') if request.POST.get('satuan') else None #id satuan

				# GET Coordinate Pengirim & Penerima
				try :
					arr_penerima = [nama_desa_penerima,nama_kecamatan_penerima,nama_kota_penerima,nama_provinsi_penerima]
					arr_pengirim = [nama_desa_pengirim,nama_kecamatan_pengirim,nama_kota_pengirim,nama_provinsi_pengirim]					
					coordinat_penerima, extra_cash_penerima, provinsi_terima = get_location(arr_alamat=arr_penerima, URL_GEO=URL_GEO, API_GEO=API_GEO)
					coordinat_pengirim, extra_cash_pengirim, provinsi_kirim = get_location(arr_alamat=arr_pengirim, URL_GEO=URL_GEO, API_GEO=API_GEO)
					print("KOORDINAT PENERIMA", coordinat_penerima, extra)
					print("KOORDINAT PENGIRIM", coordinat_pengirim)
				except Exception as e: 
					raise Exception("Gagal memperoleh koordinat penerima dan pengirim, {}".format(str(e)))

				outlet_pengiriman = request.POST.get('outlet_pengiriman')
				try :
					outlet1 = model_to_dict(get_object_or_404(Toko, id=outlet_pengiriman))
				except :
					raise Exception('Tidak dapat menemukan Outlet Pengiriman di database, outlet dikirimkan = {outlet}'.format(outlet_pengiriman))

				titik_lokasi_outlet_1 = outlet1['titik_lokasi'].split(",")

				outlet_list = list(Toko.objects.filter(is_active=True).values())
				if not outlet_list :
					raise Exception('Data outlet tidak tersedia') 

				outlet2_jarak_terdekat = []
				id_outlet = []

				for data in outlet_list:
					coor = data['titik_lokasi'].split(",")
					jarak = hitung_jarak([float(coor[0]), float(coor[1])], [coordinat_penerima[1], coordinat_penerima[0]])
					outlet2_jarak_terdekat.append(jarak)
					id_outlet.append(data['id'])

				index_terdekat = outlet2_jarak_terdekat.index(min(outlet2_jarak_terdekat))
				id_terdekat = id_outlet[index_terdekat] #id Toko Terdekat dengan penerima

				try :
					outlet2 = model_to_dict(get_object_or_404(Toko, id=id_terdekat))
				except :
					raise Exception('Tidak dapat menemukan Outlet Penerimaan di database, outlet dikirimkan = {outlet}'.format(id_terdekat))

				titik_lokasi_outlet_2 = outlet2['titik_lokasi'].split(",")

				titik_tengah_lokasi_outlet = get_center_coordinate([float(titik_lokasi_outlet_1[0]),float(titik_lokasi_outlet_1[1])], [float(titik_lokasi_outlet_2[0]), float(titik_lokasi_outlet_2[1])])
				titik_terdekat_gudang_1 = get_center_coordinate([float(titik_lokasi_outlet_1[0]),float(titik_lokasi_outlet_1[1])], titik_tengah_lokasi_outlet)
				titik_terdekat_gudang_2 = get_center_coordinate([float(titik_lokasi_outlet_2[0]), float(titik_lokasi_outlet_2[1])], titik_tengah_lokasi_outlet)
				
				gudang_list = list(Gudang.objects.filter(is_active=True).values())
				gudang1_jarak_terdekat = []
				id_gudang_1 = []
				gudang2_jarak_terdekat = []
				id_gudang_2 = []
				for data in gudang_list:
					coor = data['titik_lokasi'].split(",")
					jarak_gudang1 = hitung_jarak([float(coor[0]), float(coor[1])], titik_terdekat_gudang_1)
					jarak_gudang2 = hitung_jarak([float(coor[0]), float(coor[1])], titik_terdekat_gudang_2)
					
					gudang1_jarak_terdekat.append(jarak_gudang1)
					id_gudang_1.append(data['id'])

					gudang2_jarak_terdekat.append(jarak_gudang2)
					id_gudang_2.append(data['id'])

				index_terdekat_gudang_1 = gudang1_jarak_terdekat.index(min(gudang1_jarak_terdekat))
				index_terdekat_gudang_2 = gudang2_jarak_terdekat.index(min(gudang2_jarak_terdekat))

				id_gudang_pengiriman = id_gudang_1[index_terdekat_gudang_1]
				id_gudang_penerimaan = id_gudang_2[index_terdekat_gudang_2]

				jarak_outlet_1_ke_penerima = hitung_jarak([float(titik_lokasi_outlet_1[0]),float(titik_lokasi_outlet_1[1])],[coordinat_penerima[1], coordinat_penerima[0]])
				tarif_kilometer = get_harga_kilometer(jarak_outlet_1_ke_penerima)
				tarif_berat = get_harga_berat(berat)
				tarif_gudang = get_harga_gudang(id_gudang_pengiriman,id_gudang_penerimaan)
				# Get tarif Pengemasan berdasarkan ID pengemasan yang dikirim
				try :
					tarif_pengemasan = get_harga_pengemasan(pengemasan)
					if 'harga' in tarif_pengemasan :
						tarif_pengemasan = tarif_pengemasan['harga']
					else :
						tarif_pengemasan = 0
				except Exception as e : 
					tarif_pengemasan = 0

				# Get extra cash penerima berdasarkan koordinat
				keterangan_extra_tarif = []
				if extra_cash_penerima : 
					try :
						tarif_extra_penerima = get_extra_tarif(extra_cash_penerima)
						if 'harga' in tarif_extra_penerima : 
							tarif_extra_penerima = tarif_extra_penerima['harga']
							keterangan_extra_tarif.append("Alamat Penerima Kena Extra Cash(" + str(extra_cash_penerima) + ")")
						else :
							tarif_extra_penerima = 0
					except :
						tarif_extra_penerima = 0
				else:
					tarif_extra_penerima = 0

				# Get extra cash pengirim berdasarkan koordinat
				if extra_cash_pengirim : 
					try :
						tarif_extra_pengirim = get_extra_tarif(extra_cash_pengirim)
						if 'harga' in tarif_extra_pengirim : 
							tarif_extra_pengirim = tarif_extra_pengirim['harga']
							keterangan_extra_tarif.append("Alamat Pengirim Kena Extra Cash(" + str(extra_cash_pengirim) + ")")
						else :
							tarif_extra_pengirim = 0
					except :
						tarif_extra_pengirim = 0
				else:
					tarif_extra_pengirim = 0

				# Gabung kata jika ada extra tarif
				if keterangan_extra_tarif and len(keterangan_extra_tarif) :
					if len(keterangan_extra_tarif) == 1 :
						"".join(keterangan_extra_tarif)
					else :
						" & ".join(keterangan_extra_tarif)
				else :
					keterangan_extra_tarif = None

				# Get tarif layanan
				try :
					tarif_layanan = get_tarif_layanan(layanan)
					if 'harga' in tarif_layanan : 
						tarif_layanan = tarif_layanan['harga']
					else :
						tarif_layanan = 0
				except : 
					tarif_layanan = 0

				total_all_tarif = tarif_layanan + tarif_kilometer + tarif_berat + tarif_gudang + tarif_extra_penerima
				total_all_tarif = int(total_all_tarif)
				# Usahakan semua source diisi dengan keterangan yang konsisten
				source = 'api_order_pickup'

				data_to_insert = {
					'id_toko' : outlet1['id'],
					'id_gudang' : id_gudang_pengiriman,
					'nama_pengirim' : nama_pengirim,
					'no_tlp_pengirim' : no_telp_pengirim,
					'alamat_pengirim' : alamat_pengirim,
					'provinsi_pengirim' : provinsi_pengirim,
					'kota_pengirim' : kota_pengirim,
					'kecamatan_pengirim' : kecamatan_pengirim,
					'desa_pengirim' : desa_pengirim,
					'kode_pos_pengirim' : kode_pos_pengirim,

					'id_toko2' : outlet2['id'],
					'id_gudang2' : id_gudang_penerimaan,
					'nama_penerima' : nama_penerima,
					'no_tlp_penerima' : no_telp_penerima,
					'alamat_penerima' : alamat_penerima,
					'provinsi_penerima' : provinsi_penerima,
					'kota_penerima' : kota_penerima,
					'kecamatan_penerima' : kecamatan_penerima,
					'desa_penerima' : desa_penerima,
					'kode_pos_penerima' : kode_pos_penerima,
					'status_pengirim' : status_pengirim,

					'jenis_barang' : jenis_barang,
					'detail_barang' : detail_barang,
					'id_pengemasan' : pengemasan,
					'jenis_pengiriman' : layanan,
					'berat' : berat,
					'jumlah' : jumlah,
					'satuan' : satuan,

					'tarif_berat' : tarif_berat,
					'tarif_kilometer': tarif_kilometer,
					'tarif_gudang' : tarif_gudang,
					'tarif_layanan' : tarif_layanan,
					'extra_tarif_penerima' : tarif_extra_penerima,
					'extra_tarif_pengirim' : tarif_extra_pengirim,
					'keterangan_extra_tarif' : keterangan_extra_tarif,
					'total_tarif' : total_all_tarif,
				}

				if request.POST.get('email_penerima') :
					data_to_insert['email_penerima'] = request.POST.get('email_penerima')

				form = PelangganOrderPickupForm(data=data_to_insert)

				if form.is_valid():
					new_order = form.save(commit=False)
					new_order.id_order = generate_id('OP', 8)
					new_order.save()
					data_order = model_to_dict(new_order)

					data_order = {'no_order':data_order['id_order'], 'total_tagihan':data_order['total_tarif']}

					result['data']={'data_order':data_order,'lokasi_penerima': coordinat_penerima, 'lokasi_pengirim': coordinat_pengirim, 'tarif_kilometer': tarif_kilometer, 'tarif_berat': tarif_berat, 'tarif_gudang': tarif_gudang}
					result['msg'] = 'Sukses'
					result['status'] = 200
				else :
					result['msg'] = 'Terjadi Kesalahan: form order tidak valid'
					result['status'] = 400
					result['error'] = form.errors
					return JsonResponse({'result': result}, status=result['status'])
					
				# Gudang_penerimaan
			except Exception as e :
				result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
				result['status'] = 422
			
			return JsonResponse({'result': result}, status=result['status'])
			# else:
			# 	result['msg'] = 'Otentikasi Gagal'
			# 	result['status'] = 401
			# 	return JsonResponse({'result': result}, status=result['status'])
		except Exception as e:
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 400
			return JsonResponse({'result': result}, status=result['status'])


class OrderPickupAPI(APIView):
	def post(self, request):
		# Under construction
		result = {
			'data': [],
			'msg': '',
			'status': 200,
		}

		try :
			URL_GEO = 'https://api.openrouteservice.org/geocode/search?'
			API_GEO = CONF.API_OPEN_ROUTE_SERVICE

			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(username=username, password=password)
			if user:
				kode_pos_pengirim = request.POST.get('kode_pos_pengirim')
				kode_pos_penerima = request.POST.get('kode_pos_penerima')

				try:
					data_pengirim = KodePos.objects.filter(kode_pos = kode_pos_pengirim).first()
					data_penerima = KodePos.objects.filter(kode_pos = kode_pos_penerima).first()
					if not data_pengirim or not data_penerima :
						raise Exception('Tidak dapat menemukan kode pos penerima atau pengirim')

					provinsi_penerima = data_penerima.provinsi_id.id
					kota_penerima = data_penerima.kota_id.id
					kecamatan_penerima = data_penerima.kecamatan_id.id
					desa_penerima = data_penerima.desa_id.id

					nama_provinsi_penerima = data_penerima.provinsi_id.nama_provinsi
					nama_kota_penerima = data_penerima.kota_id.nama_kota
					nama_kecamatan_penerima = data_penerima.kecamatan_id.nama_kecamatan
					nama_desa_penerima = data_penerima.desa_id.nama_desa

					provinsi_pengirim = data_pengirim.provinsi_id.id
					kota_pengirim = data_pengirim.kota_id.id
					kecamatan_pengirim = data_pengirim.kecamatan_id.id
					desa_pengirim = data_pengirim.desa_id.id

					nama_provinsi_pengirim = data_pengirim.provinsi_id.nama_provinsi
					nama_kota_pengirim = data_pengirim.kota_id.nama_kota
					nama_kecamatan_pengirim = data_pengirim.kecamatan_id.nama_kecamatan
					nama_desa_pengirim = data_pengirim.desa_id.nama_desa

					alamat_pengirim = request.POST.get('alamat_pengirim')
					alamat_penerima = request.POST.get('alamat_penerima')
					nama_pengirim = request.POST.get('nama_pengirim')
					nama_penerima = request.POST.get('nama_penerima')
					status_pengirim = request.POST.get('status_pengirim')
					no_telp_pengirim = request.POST.get('no_telp_pengirim')
					no_telp_penerima = request.POST.get('no_telp_penerima')

					jenis_barang = request.POST.get('jenis_barang')
					detail_barang = request.POST.get('detail_barang')
					pengemasan = request.POST.get('pengemasan') #id pengemasan
					layanan = request.POST.get('layanan') #id layanan
					berat = request.POST.get('berat') if request.POST.get('berat') else '0'
					jumlah = request.POST.get('jumlah')
					satuan = request.POST.get('satuan') if request.POST.get('satuan') else None #id satuan

					# GET Coordinate Pengirim & Penerima
					try :
						arr_penerima = [nama_desa_penerima,nama_kecamatan_penerima,nama_kota_penerima,nama_provinsi_penerima]
						arr_pengirim = [nama_desa_pengirim,nama_kecamatan_pengirim,nama_kota_pengirim,nama_provinsi_pengirim]					
						coordinat_penerima, extra_cash_penerima, provinsi_terima = get_location(arr_alamat=arr_penerima, URL_GEO=URL_GEO, API_GEO=API_GEO)
						coordinat_pengirim, extra_cash_pengirim, provinsi_kirim = get_location(arr_alamat=arr_pengirim, URL_GEO=URL_GEO, API_GEO=API_GEO)
					except Exception as e: 
						raise Exception("Gagal memperoleh koordinat penerima dan pengirim, {}".format(str(e)))


					outlet_pengiriman = request.POST.get('outlet_pengiriman')
					try :
						outlet1 = model_to_dict(get_object_or_404(Toko, id=outlet_pengiriman))
					except :
						raise Exception('Tidak dapat menemukan Outlet Pengiriman di database, outlet dikirimkan = {outlet}'.format(outlet_pengiriman))

					titik_lokasi_outlet_1 = outlet1['titik_lokasi'].split(",")

					outlet_list = list(Toko.objects.filter(is_active=True).values())
					if not outlet_list :
						raise Exception('Data outlet tidak tersedia') 

					outlet2_jarak_terdekat = []
					id_outlet = []

					for data in outlet_list:
						coor = data['titik_lokasi'].split(",")
						jarak = hitung_jarak([float(coor[0]), float(coor[1])], [coordinat_penerima[1], coordinat_penerima[0]])
						outlet2_jarak_terdekat.append(jarak)
						id_outlet.append(data['id'])

					index_terdekat = outlet2_jarak_terdekat.index(min(outlet2_jarak_terdekat))
					id_terdekat = id_outlet[index_terdekat] #id Toko Terdekat dengan penerima

					try :
						outlet2 = model_to_dict(get_object_or_404(Toko, id=id_terdekat))
					except :
						raise Exception('Tidak dapat menemukan Outlet Penerimaan di database, outlet dikirimkan = {outlet}'.format(id_terdekat))

					titik_lokasi_outlet_2 = outlet2['titik_lokasi'].split(",")

					titik_tengah_lokasi_outlet = get_center_coordinate([float(titik_lokasi_outlet_1[0]),float(titik_lokasi_outlet_1[1])], [float(titik_lokasi_outlet_2[0]), float(titik_lokasi_outlet_2[1])])
					titik_terdekat_gudang_1 = get_center_coordinate([float(titik_lokasi_outlet_1[0]),float(titik_lokasi_outlet_1[1])], titik_tengah_lokasi_outlet)
					titik_terdekat_gudang_2 = get_center_coordinate([float(titik_lokasi_outlet_2[0]), float(titik_lokasi_outlet_2[1])], titik_tengah_lokasi_outlet)
					
					gudang_list = list(Gudang.objects.filter(is_active=True).values())
					gudang1_jarak_terdekat = []
					id_gudang_1 = []
					gudang2_jarak_terdekat = []
					id_gudang_2 = []
					for data in gudang_list:
						coor = data['titik_lokasi'].split(",")
						jarak_gudang1 = hitung_jarak([float(coor[0]), float(coor[1])], titik_terdekat_gudang_1)
						jarak_gudang2 = hitung_jarak([float(coor[0]), float(coor[1])], titik_terdekat_gudang_2)
						
						gudang1_jarak_terdekat.append(jarak_gudang1)
						id_gudang_1.append(data['id'])

						gudang2_jarak_terdekat.append(jarak_gudang2)
						id_gudang_2.append(data['id'])

					index_terdekat_gudang_1 = gudang1_jarak_terdekat.index(min(gudang1_jarak_terdekat))
					index_terdekat_gudang_2 = gudang2_jarak_terdekat.index(min(gudang2_jarak_terdekat))

					id_gudang_pengiriman = id_gudang_1[index_terdekat_gudang_1]
					id_gudang_penerimaan = id_gudang_2[index_terdekat_gudang_2]

					jarak_outlet_1_ke_penerima = hitung_jarak([float(titik_lokasi_outlet_1[0]),float(titik_lokasi_outlet_1[1])],[coordinat_penerima[1], coordinat_penerima[0]])
					tarif_kilometer = get_harga_kilometer(jarak_outlet_1_ke_penerima)
					tarif_berat = get_harga_berat(berat)
					tarif_gudang = get_harga_gudang(id_gudang_pengiriman,id_gudang_penerimaan)
					# Get tarif Pengemasan berdasarkan ID pengemasan yang dikirim
					try :
						tarif_pengemasan = get_harga_pengemasan(pengemasan)
						if 'harga' in tarif_pengemasan :
							tarif_pengemasan = tarif_pengemasan['harga']
						else :
							tarif_pengemasan = 0
					except Exception as e : 
						tarif_pengemasan = 0

					# Get extra cash penerima berdasarkan koordinat
					keterangan_extra_tarif = []
					if extra_cash_penerima : 
						try :
							tarif_extra_penerima = get_extra_tarif(extra_cash_penerima)
							if 'harga' in tarif_extra_penerima : 
								tarif_extra_penerima = tarif_extra_penerima['harga']
								keterangan_extra_tarif.append("Alamat Penerima Kena Extra Cash(" + str(extra_cash_penerima) + ")")
							else :
								tarif_extra_penerima = 0
						except :
							tarif_extra_penerima = 0
					else:
						tarif_extra_penerima = 0

					# Get extra cash pengirim berdasarkan koordinat
					if extra_cash_pengirim : 
						try :
							tarif_extra_pengirim = get_extra_tarif(extra_cash_pengirim)
							if 'harga' in tarif_extra_pengirim : 
								tarif_extra_pengirim = tarif_extra_pengirim['harga']
								keterangan_extra_tarif.append("Alamat Pengirim Kena Extra Cash(" + str(extra_cash_pengirim) + ")")
							else :
								tarif_extra_pengirim = 0
						except :
							tarif_extra_pengirim = 0
					else:
						tarif_extra_pengirim = 0

					# Gabung kata jika ada extra tarif
					if keterangan_extra_tarif and len(keterangan_extra_tarif) :
						if len(keterangan_extra_tarif) == 1 :
							"".join(keterangan_extra_tarif)
						else :
							" & ".join(keterangan_extra_tarif)
					else :
						keterangan_extra_tarif = None

					# Get tarif layanan
					try :
						tarif_layanan = get_tarif_layanan(layanan)
						if 'harga' in tarif_layanan : 
							tarif_layanan = tarif_layanan['harga']
						else :
							tarif_layanan = 0
					except : 
						tarif_layanan = 0

					total_all_tarif = tarif_layanan + tarif_kilometer + tarif_berat + tarif_gudang + tarif_extra_penerima
					total_all_tarif = int(total_all_tarif)
					# Usahakan semua source diisi dengan keterangan yang konsisten
					source = 'api_order_pickup'

					data_to_insert = {
						'id_toko' : outlet1['id'],
						'id_gudang' : id_gudang_pengiriman,
						'nama_pengirim' : nama_pengirim,
						'no_tlp_pengirim' : no_telp_pengirim,
						'alamat_pengirim' : alamat_pengirim,
						'provinsi_pengirim' : provinsi_pengirim,
						'kota_pengirim' : kota_pengirim,
						'kecamatan_pengirim' : kecamatan_pengirim,
						'desa_pengirim' : desa_pengirim,
						'kode_pos_pengirim' : kode_pos_pengirim,

						'id_toko2' : outlet2['id'],
						'id_gudang2' : id_gudang_penerimaan,
						'nama_penerima' : nama_penerima,
						'no_tlp_penerima' : no_telp_penerima,
						'alamat_penerima' : alamat_penerima,
						'provinsi_penerima' : provinsi_penerima,
						'kota_penerima' : kota_penerima,
						'kecamatan_penerima' : kecamatan_penerima,
						'desa_penerima' : desa_penerima,
						'kode_pos_penerima' : kode_pos_penerima,

						'jenis_barang' : jenis_barang,
						'detail_barang' : detail_barang,
						'id_pengemasan' : pengemasan,
						'jenis_pengiriman' : layanan,
						'berat' : berat,
						'jumlah' : jumlah,
						'satuan' : satuan,

						'tarif_berat' : tarif_berat,
						'tarif_kilometer': tarif_kilometer,
						'tarif_gudang' : tarif_gudang,
						'tarif_layanan' : tarif_layanan,
						'extra_tarif_penerima' : tarif_extra_penerima,
						'extra_tarif_pengirim' : tarif_extra_pengirim,
						'keterangan_extra_tarif' : keterangan_extra_tarif,
						'total_tarif' : total_all_tarif,
					}

					if request.POST.get('email_penerima') :
						data_to_insert['email_penerima'] = request.POST.get('email_penerima')

					form = PelangganOrderPickupForm(data=data_to_insert)

					if form.is_valid():
						new_order = form.save(commit=False)
						new_order.id_order = generate_id('OP', 8)
						new_order.save()
						data_order = model_to_dict(new_order)

						data_order = {'no_order':data_order['id_order'], 'total_tagihan':data_order['total_tarif']}

						result['data']={'data_order':data_order,'lokasi_penerima': coordinat_penerima, 'lokasi_pengirim': coordinat_pengirim, 'tarif_kilometer': tarif_kilometer, 'tarif_berat': tarif_berat, 'tarif_gudang': tarif_gudang}
						result['msg'] = 'Sukses'
						result['status'] = 200
					else :
						result['msg'] = 'Terjadi Kesalahan: form order tidak valid'
						result['status'] = 400
						result['error'] = form.errors
						return JsonResponse({'result': result}, status=result['status'])
						
					# Gudang_penerimaan
				except Exception as e :
					result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
					result['status'] = 422
				
				return JsonResponse({'result': result}, status=result['status'])
			else:
				result['msg'] = 'Otentikasi Gagal'
				result['status'] = 401
				return JsonResponse({'result': result}, status=result['status'])
		except Exception as e:
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 400
			return JsonResponse({'result': result}, status=result['status'])
