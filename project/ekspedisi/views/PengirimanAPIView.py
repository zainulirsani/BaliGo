from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.decorators import api_view

import datetime
import numpy as np
import math
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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.conf import settings as CONF
import requests as req_api

from django.urls import reverse
from .pengiriman_ambil_data import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class PengirimanPOSAPI(APIView) :
	def post(self, request) :
		result = {
			'data': [],
			'msg': '',
			'status': 200,
		}

		try :
			try : 
				cek_pengiriman = get_object_or_404(Pengiriman, id=request.POST.get('id_pengiriman',0))
			except :
				raise Exception('Tidak dapat menemukan data pengiriman dengan ID {}'.format(request.POST.get('id_pengiriman',0)))

			data_to_insert = {
				'id_pengiriman' :request.POST.get('id_pengiriman', 0),
				'nominal_bayar' :request.POST.get('nominal_bayar', 0),
				'total_tagihan' :request.POST.get('total_tagihan', 0),
				'total_kembali' :request.POST.get('total_kembali', 0),
			}

			form = POSForm(data=data_to_insert)
			if form.is_valid() :
				data_form = form.save(commit=False)
				data_form.no_transaksi = generate_id('EP', 8)
				data_form.save()

				data_transaksi_pos = {
					'no_transaksi_pos' : data_form.no_transaksi,
					'total_tagihan' : data_form.total_tagihan,
					'nominal_bayar' : data_form.nominal_bayar,
					'total_kembali' : data_form.total_kembali
				}
				result['data']={'nomor_transaksi_pos':data_transaksi_pos}
				result['msg'] = 'Sukses'
				result['status'] = 200
				return JsonResponse({'result': result}, status=result['status'])

			else :
				result['msg'] = 'Terjadi Kesalahan: form pengiriman tidak valid'
				result['status'] = 400
				result['error'] = form.errors
				return JsonResponse({'result': result}, status=result['status'])

		except Exception as e :
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 500
			return JsonResponse({'result': result}, status=result['status'])

class PengirimanAPI(APIView):
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
					keterangan_extra_tarif = 'Alamat Penerima & Alamat Pengirim Tidak Kena Extra Cash'
					if extra_cash_penerima : 
						try :
							tarif_extra_penerima = get_extra_tarif(extra_cash_penerima)
							if 'harga' in tarif_extra_penerima : 
								tarif_extra_penerima = tarif_extra_penerima['harga']
								keterangan_extra_tarif = "Alamat Penerima Kena Extra Cash(" + str(extra_cash_penerima) + ") & Alamat Pengirim Tidak Kena Extra Cash"
							else :
								tarif_extra_penerima = 0
						except :
							tarif_extra_penerima = 0
					else:
						tarif_extra_penerima = 0

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
					source = 'api_pengiriman'

					# outlet1 --------------------0--------------------outlet2  cari titik tengah kedua outlet
					# outlet1---------------------$--------------------0        cari titik tengan outlet dengan titik tengah (0) tadi
					# gudang 1 (gudang_pengiriman) = cari gudang terdekat dengan $
					#
					# 0-------------------------&----------------------outlet2 cari titik tengah outlet2 dengan titik tengah (0)
					# gudang 2 (gudang_penerimaan) = cari gudang terdekat dengan &

					data_to_insert = {
						'outlet_pengiriman' : outlet1['id'],
						'gudang_pengiriman' : id_gudang_pengiriman,
						'nama_pengirim' : nama_pengirim,
						'no_telp_pengirim' : no_telp_pengirim,
						'alamat_pengirim' : alamat_pengirim,
						'provinsi_pengirim' : provinsi_pengirim,
						'kota_pengirim' : kota_pengirim,
						'kecamatan_pengirim' : kecamatan_pengirim,
						'desa_pengirim' : desa_pengirim,
						'kode_pos_pengirim' : data_pengirim,

						'outlet_penerimaan' : outlet2['id'],
						'gudang_penerimaan' : id_gudang_penerimaan,
						'nama_penerima' : nama_penerima,
						'no_telp_penerima' : no_telp_penerima,
						'alamat_penerima' : alamat_penerima,
						'provinsi_penerima' : provinsi_penerima,
						'kota_penerima' : kota_penerima,
						'kecamatan_penerima' : kecamatan_penerima,
						'desa_penerima' : desa_penerima,
						'kode_pos_penerima' : data_penerima,

						'jenis_barang' : jenis_barang,
						'detail_barang' : detail_barang,
						'pengemasan' : pengemasan,
						'layanan' : layanan,
						'berat' : berat,
						'jumlah' : jumlah,
						'satuan' : satuan,

						'tarif_berat' : tarif_berat,
						'tarif_kilometer': tarif_kilometer,
						'tarif_gudang' : tarif_gudang,
						'tarif_layanan' : tarif_layanan,
						'extra_tarif_penerima' : tarif_extra_penerima,
						'keterangan_extra_tarif' : keterangan_extra_tarif,
						'total_tarif' : total_all_tarif,
					}

					if request.POST.get('email_pengirim') :
						data_to_insert['email_pengirim'] = request.POST.get('email_pengirim')
					if request.POST.get('email_penerima') :
						data_to_insert['email_penerima'] = request.POST.get('email_penerima')

					form = PengirimanForm(data=data_to_insert)
					formPelacakan = LogPengirimanForm()

					if form.is_valid():
						new_pengiriman = form.save(commit=False)
						new_pengiriman.id_pengiriman = generate_id('ER', 8)
						new_pengiriman.source = source
						try : 
							new_pengiriman.api_pencatat_by_id = request.POST('api_pencatat_by_id', None)
							new_pengiriman.api_pencatat_by_user_name = request.POST('api_pencatat_by_user_name', None)
							new_pengiriman.api_source_name_apps = request.POST('api_source_name_apps', None)
							new_pengiriman.api_pengiriman_id_apps = request.POST('api_pengiriman_id_apps', None)
						except :
							pass
						new_pengiriman.save()

						new_pelacakan = formPelacakan.save(commit=False)
						new_pelacakan.id_pengiriman = get_object_or_404(Pengiriman, id_pengiriman=new_pengiriman)
						new_pelacakan.rute_pengiriman_outlet = get_object_or_404(Toko, id=outlet1['id'])
						new_pelacakan.rute_pengiriman_outlet_akhir = get_object_or_404(Toko, id=outlet2['id'])
						new_pelacakan.rute_pengiriman_gudang = get_object_or_404(Gudang, id=id_gudang_pengiriman)
						new_pelacakan.rute_pengiriman_gudang_akhir = get_object_or_404(Gudang, id=id_gudang_penerimaan)
						new_pelacakan.status_pengiriman = 'waiting'
						try :
							new_pelacakan.api_kurir_id = request.POST.get('api_kurir_id')
							new_pelacakan.api_kurir_name = request.POST.get('api_kurir_name')
						except :
							pass

						new_pelacakan.save()
						data_pengiriman = {'resi':new_pengiriman.id_pengiriman, 'total_tagihan':new_pengiriman.total_tarif}

						result['data']={'data_pengiriman':data_pengiriman,'lokasi_penerima': coordinat_penerima, 'lokasi_pengirim': coordinat_pengirim, 'tarif_kilometer': tarif_kilometer, 'tarif_berat': tarif_berat, 'tarif_gudang': tarif_gudang}
						result['msg'] = 'Sukses'
						result['status'] = 200
					else :
						result['msg'] = 'Terjadi Kesalahan: form pengiriman tidak valid'
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

class PengirimanUpdateStatusAPI(APIView):
	def post(self, request):
		result = {
			'data': [],
			'msg': '',
			'status': 200,
		}

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
					# raise Exception('Titik lokasi tidak boleh kosong, pastikan anda sudah mengirim titik lokasi yang valid')
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
				api_kurir_id = request.POST.get('api_kurir_id'),
				api_kurir_name = request.POST.get('api_kurir_name'),
				status_pengiriman = status,
			)

			log_new.save()

			result['data']={'titik_lokasi':titik_lokasi, 'status_pengiriman_disimpan':status}
			result['msg'] = 'Sukses'
			result['status'] = 200

			return JsonResponse({'result': result}, status=result['status'])
		except Exception as e:
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 400
			return JsonResponse({'result': result}, status=result['status'])

class PengirimanStatusTerkini(APIView) :
	def post(self, request) :
		result = {
			'data': [],
			'msg': '',
			'status': 200,
		}

		try :
			id_pengiriman = request.POST.get('id_pengiriman')
			log_terakhir = LogPengiriman.objects.filter(id_pengiriman_id=id_pengiriman).order_by('-pk')

			if log_terakhir.exists() :
				result['data'] = list(log_terakhir.values())
				result['msg'] = 'Sukses'

			else :
				result['data'] = []
				result['msg'] = 'Sukses'
				
			return JsonResponse({'result': result}, status=result['status'])
		except Exception as e :
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 400
			return JsonResponse({'result': result}, status=result['status'])

def get_outlet(lat, lon):
	result = {
		'data': [],
		'msg': '',
		'status': 200,
	}

	try:
		datas = list(Toko.objects.values().filter(is_active = True))
		data_jarak = [];
		for data in datas:
			loc_toko = data['titik_lokasi'].split(',') #lat, lon
			jarak = hitung_jarak([float(lat), float(lon)], [float(loc_toko[0]), float(loc_toko[1])])
			data_jarak.append(jarak);
		index_minimum = data_jarak.index(min(data_jarak))
		outlet_terpilih = datas[index_minimum]
		result['data'] = outlet_terpilih
		result['msg'] = 'sukses'
	except Exception as e:
		result['msg'] = 'terjadi kesalahan : {}'.format(e)
		result['status'] = '422'
	
	return result

def get_gudang(lat, lon):
	result = {
		'data': [],
		'msg': '',
		'status': 200,
	}

	try:
		datas = list(Gudang.objects.values().filter(is_active = True))
		data_jarak = [];
		for data in datas:
			loc_gudang = data['titik_lokasi'].split(',') #lat, lon
			jarak = hitung_jarak([float(lat), float(lon)], [float(loc_gudang[0]), float(loc_gudang[1])])
			data_jarak.append(jarak);
		index_minimum = data_jarak.index(min(data_jarak))
		gudang_terpilih = datas[index_minimum]
		result['data'] = gudang_terpilih
		result['msg'] = 'sukses'
	except Exception as e:
		result['msg'] = 'terjadi kesalahan : {}'.format(e)
		result['status'] = '422'
	
	return result

def get_gudang_by_province(province):
	result = {
		'data': [],
		'msg': '',
		'status': 200,
	}

	try:
		data = model_to_dict(Gudang.objects.filter(is_active = True, provinsi_gudang=province).first())

		result['data'] = data
		result['msg'] = 'sukses'
	except Exception as e:
		result['msg'] = 'terjadi kesalahan : {}'.format(e)
		result['status'] = '422'
	
	return result


def get_list_layanan(tarif_berat, tarif_kilometer, tarif_gudang, tarif_pengemasan, tarif_extra_penerima):
	result = {
		'data': [],
		'msg': '',
		'status': 200,
	}
	try:
		tarif_layanan = list(TarifLayanan.objects.filter(is_active=True).prefetch_related('tarif_layanan_nama').values())
		tarif_layanan = list(TarifLayanan.objects.filter(is_active=True).values())
		data_list = []

		for data in tarif_layanan:
			layanan = model_to_dict(get_object_or_404(Layanan, id = data['layanan_id']))
			if layanan['publish_status'] == True:
				data_list.append({'id_tarif_layanan': data['id_tarif_layanan'], 'nama_layanan': layanan['nama_layanan'], 'harga': int(data['tarif']) + tarif_berat + tarif_kilometer + tarif_gudang + tarif_pengemasan + tarif_extra_penerima, 'estimasi': layanan['estimasi_layanan']})

		result['data'] = data_list
		result['msg'] = 'sukses'
	except Exception as e:
		result['msg'] = 'terjadi kesalahan :  {}'.format(e)
		result['status'] = 422
	return result

def get_location(arr_alamat, URL_GEO, API_GEO):
	location = []
	loc_data = ['desa', 'kecamatan', 'kota', 'provinsi']
	extra_cash = ''
	i = 0
	province = ''
	for i in range(len(arr_alamat)):
		if i == 0:
			alamat_cari = arr_alamat[:]
		else:
			alamat_cari = arr_alamat[i:]
		region = ','.join(alamat_cari)
		
		PARAMS = {'api_key': API_GEO, 'text': region, 'size': '1', 'country': 'IDN'}
		r = req_api.get(url = URL_GEO, params = PARAMS)
		data = r.json()
		if not len(data['features']) : # check jika kosong
			continue
		else:
			location = data['features'][0]['geometry']['coordinates']
			province = data['features'][0]['properties']['region']
			if i > 0:
				extra_cash = loc_data[i]
			else:
				extra_cash = ''
			break
	return location, extra_cash, province

def get_harga_kilometer(kilometer):
	list_harga = list(TarifKilometer.objects.filter(is_active=True).values())
	#Jika ada banyak list tarif kilometer, maka cari harga dengan kilometer terdekat dengan kilometer yg di input 
				
	jarak_terdekat = []
	id_tarif = []
	for data in list_harga:
		jarak = math.sqrt(math.pow((int(data['jarak'])-round(float(kilometer))), 2)) #eucledian distance
		jarak_terdekat.append(jarak)
		id_tarif.append(data['id'])

	index_terdekat = jarak_terdekat.index(min(jarak_terdekat))
	id_terdekat = id_tarif[index_terdekat] #id tarif kilometer yang digunakan untuk dikalikan dengan kilometer input

	tarif_yang_digunakan = model_to_dict(get_object_or_404(TarifKilometer, id = id_terdekat))
	harga_mentah = float(tarif_yang_digunakan['tarif']) * round(float(kilometer))
	harga = round(harga_mentah / int(tarif_yang_digunakan['jarak']))
	return harga

def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]

def get_harga_kilometer_new(kilometer):
	print('JARAKNYA', kilometer)
	harga = 0
	try:
		if kilometer == '0' or kilometer == 0:
			return harga
		else:
			list_harga = list(TarifKilometer.objects.filter(is_active=True).values_list('jarak', flat=True))
			#Jika ada banyak list tarif kilometer, maka cari harga dengan kilometer terdekat dengan kilometer yg di input 
			
			jarak_terdekat = []
			id_tarif = []
			# for data in list_harga:
			# 	jarak = math.sqrt(math.pow((int(data['jarak'])-round(float(kilometer))), 2)) #eucledian distance
			# 	jarak_terdekat.append(jarak)
			# 	id_tarif.append(data['id'])

			#index_terdekat = jarak_terdekat.index(min(jarak_terdekat))
			#id_terdekat = id_tarif[index_terdekat] #id tarif kilometer yang digunakan untuk dikalikan dengan kilometer input

			try :
				jarak_terdekat_aktif = closest(list_harga, int(round(float(kilometer))))
				tarif_yang_digunakan = TarifKilometer.objects.filter(jarak=jarak_terdekat_aktif).latest('updated_at')
				if tarif_yang_digunakan :
					id_terdekat = tarif_yang_digunakan.id
					harga_mentah = float(tarif_yang_digunakan.tarif) * int(round(float(kilometer)))
					harga = round(harga_mentah / int(tarif_yang_digunakan.jarak))
				else :
					id_terdekat = 0
					tarif_yang_digunakan = 0
					harga = 0
			except Exception as e :
				print(e)
				raise Exception('Tidak menemukan tarif kilometer terdekat atau yang aktif')
			return harga
	except Exception as e:
		return harga

def get_harga_berat(berat):
	list_harga = list(TarifBerat.objects.filter(is_active=True).values())
	#Jika ada banyak list Tarif Berat, maka cari harga dengan berat terdekat dengan berat yg di input 
				
	jarak_terdekat = []
	id_tarif = []
	for data in list_harga:
		jarak = math.sqrt(math.pow((float(data['berat'])-float(berat)), 2)) #eucledian distance
		jarak_terdekat.append(jarak)
		id_tarif.append(data['id'])

	index_terdekat = jarak_terdekat.index(min(jarak_terdekat))
	id_terdekat = id_tarif[index_terdekat] #id Tarif Berat yang digunakan untuk dikalikan dengan berat input

	tarif_yang_digunakan = model_to_dict(get_object_or_404(TarifBerat, id = id_terdekat))
	harga = float(tarif_yang_digunakan['tarif']) * float(berat)
	return harga

def get_harga_berat_new(berat):
	harga = 0
	try:
		if berat == '0' or berat == 0:
			return harga
		else:
			list_harga = list(TarifBerat.objects.filter(is_active=True).values())
			#Jika ada banyak list Tarif Berat, maka cari harga dengan berat terdekat dengan berat yg di input 
			
			jarak_terdekat = []
			id_tarif = []
			for data in list_harga:
				jarak = math.sqrt(math.pow((float(data['berat'])-float(berat)), 2)) #eucledian distance
				jarak_terdekat.append(jarak)
				id_tarif.append(data['id'])

			index_terdekat = jarak_terdekat.index(min(jarak_terdekat))
			id_terdekat = id_tarif[index_terdekat] #id Tarif Berat yang digunakan untuk dikalikan dengan berat input

			try :
				tarif_yang_digunakan = model_to_dict(TarifBerat.objects.filter(berat=int(berat), is_active=1).latest('created_at'))
				harga = float(float(int(tarif_yang_digunakan['tarif']) / float(tarif_yang_digunakan['berat'])) * int(berat))
			except Exception as e:
				print(e)
				tarif_yang_digunakan = model_to_dict(get_object_or_404(TarifBerat, id = id_terdekat))
				# harga = float(tarif_yang_digunakan['tarif']) * float(berat)
				harga = float(float(int(tarif_yang_digunakan['tarif']) / float(tarif_yang_digunakan['berat'])) * int(berat))
			
			return harga
	except Exception as e:
		return harga

def get_extra_tarif(region):
	data = {
		'nama_extra': 'Tidak Kena Extra Tarif',
		'harga': 0,
		'msg': '',
		'status': 200
	}
	try:
		if region:
			extra_cash = model_to_dict(get_object_or_404(ExtraCash, wilayah = region, is_active=True))
			harga = float(extra_cash['tarif'])
			data['nama_extra'] = region
			data['harga'] = harga
			data['msg'] = 'Sukses Ambil Data'
		else:
			data['nama_extra'] = 'Tidak Kena Extra Tarif'
			data['harga'] = 0
			data['msg'] = 'Sukses Ambil Data'
	except Exception as e:
		data['nama_extra'] = 'Tidak Kena Extra Tarif'
		data['harga'] = 0
		data['msg'] = 'Gagal Ambil Data, {}'.format(e)
		data['status'] = 422
	return data

def get_harga_pengemasan(id_pengemasan):
	data = {
		'nama_pengemasan': 'Tanpa Pengemasan',
		'harga': 0,
		'msg': '',
		'status': 200
	}
	try:
		pengemasan = model_to_dict(get_object_or_404(Pengemasan, id = id_pengemasan, is_active=True))
		nama_pengemasan = pengemasan['nama_pengemasan']
		harga = float(pengemasan['tarif'])
		data['nama_pengemasan'] = nama_pengemasan
		data['harga'] = harga
		data['msg'] = 'Sukses Ambil Data'
	except Exception as e:
		data['nama_pengemasan'] = 'Tanpa Pengemasan'
		data['harga'] = 0
		data['msg'] = 'Gagal Ambil Data, {}'.format(e)
		data['status'] = 422
	return data

def get_tarif_layanan(id_layanan):
	data = {
		'nama_layanan': 'Tidak Diketahui',
		'harga': 0,
		'msg': '',
		'status': 200
	}
	try:
		layanan = get_object_or_404(Layanan, id = id_layanan, is_active=True)
		nama_layanan = layanan.nama_layanan
		harga = layanan.tarif_layanan_nama.filter(is_active=True).order_by('-pk')
		if harga.exists() :
			harga = float(harga.first().tarif)
		else :
			harga = 0
		data['nama_layanan'] = nama_layanan
		data['harga'] = harga
		data['msg'] = 'Sukses Ambil Data'
	except Exception as e:
		data['nama_layanan'] = 'Tidak Diketahui'
		data['harga'] = 0
		data['msg'] = 'Gagal Ambil Data, {}'.format(e)
		data['status'] = 422
	return data

def get_harga_gudang(gudang1, gudang2):
	tarif = list(TarifGudang.objects.filter(Q(is_active=True) & (Q(from_gudang_id=gudang1, to_gudang_id=gudang2) | Q(from_gudang_id=gudang2, to_gudang_id=gudang1))).values())

	if tarif:
		return tarif[0]
	else:
		return 0

def deg2rad(deg):
	return deg * (math.pi/180)

def rad2deg(rad):
	return rad * (180/math.pi)

# def hitung_jarak(coordinate1, coordinate2): # example array pass to this function [lat, lon]
# 	# approximate radius of earth in km
# 	R = 6373.0

# 	dlon = deg2rad(float(coordinate2[1]) - float(coordinate1[1]))
# 	dlat = deg2rad(float(coordinate2[0]) - float(coordinate1[0]))

# 	a = math.sin(dlat / 2)**2 + math.cos(coordinate1[0]) * math.cos(coordinate2[0]) * math.sin(dlon / 2)**2
# 	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# 	distance = R * c
# 	return distance

def hitung_jarak(coordinate1, coordinate2):
	r = 6371
	phi1 = np.radians(coordinate1[0])
	phi2 = np.radians(coordinate2[0])
	delta_phi = np.radians(coordinate2[0] - coordinate1[0])
	delta_lambda = np.radians(coordinate2[1] - coordinate1[1])
	a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
	res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
	return np.round(res, 2)

def get_center_coordinate(coordinate1, coordinate2):
	sumX = 0
	sumY = 0
	sumZ = 0
	lat = 0
	lng = 0

	for i in range(2):
		if i == 0:
			lat = deg2rad(coordinate1[0])
			lng = deg2rad(coordinate1[1])
		else:
			lat = deg2rad(coordinate2[0])
			lng = deg2rad(coordinate2[1])
		sumX += math.cos(lat) * math.cos(lng)
		sumY += math.cos(lat) * math.sin(lng)
		sumZ += math.sin(lat)

	avgX = sumX / 2
	avgY = sumY / 2
	avgZ = sumZ / 2

	lng = math.atan2(avgY, avgX)
	hyp = math.sqrt((avgX * avgX) + (avgY * avgY))
	lat = math.atan2(avgZ, hyp)

	return [rad2deg(lat), rad2deg(lng)]


class CekTarifAPI(View):
	def get(self, request):
		URL_GEO = 'https://api.openrouteservice.org/geocode/search?'
		API_GEO = CONF.API_OPEN_ROUTE_SERVICE
		# result = {
		# 	'data': [],
		# 	'pengemasan': '',
		# 	'tarif_berat': 0,
		# 	'tarif_kilometer': 0,
		# 	'tarif_gudang': 0,
		# 	'tarif_pengemasan': 0,
		# 	# 'extra_tarif_pengirim': 0,
		# 	'extra_tarif_penerima': 0,
		# 	'msg': '',
		# 	'status': 200,
		# }
		result = {
			'data': [],
			'pengemasan': '',
			'msg': '',
			'status': 200,
		}
		nama_provinsi_penerima = ''
		nama_kota_penerima = ''
		nama_kecamatan_penerima = ''
		nama_desa_penerima = ''

		nama_provinsi_pengirim = ''
		nama_kota_pengirim = ''
		nama_kecamatan_pengirim = ''
		nama_desa_pengirim = ''

		try:
			kode_pos_pengirim = request.GET.get('kode_pos_pengirim')
			kode_pos_penerima = request.GET.get('kode_pos_penerima')

			alamat1 = request.GET.get('alamat1', '')
			alamat2 = request.GET.get('alamat2', '')
			berat = float(request.GET.get('berat', '0'))
			pengemasan = request.GET.get('pengemasan', 0)
			extra_tarif = request.GET.get('extra_tarif', False)

			if kode_pos_pengirim and kode_pos_penerima:
				data_pengirim = KodePos.objects.filter(kode_pos = kode_pos_pengirim).first()
				data_penerima = KodePos.objects.filter(kode_pos = kode_pos_penerima).first()
				if not data_pengirim and not data_penerima:
					result['status'] = 404
					result['msg'] = 'Tidak dapat menemukan kode pos'
					raise Exception('Tidak dapat menemukan kode pos')

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

			if (alamat1 != '' and alamat2 != '') or (nama_kota_penerima != '' and nama_kota_pengirim != ''):
				if nama_kota_penerima and nama_kota_pengirim:
					arr_penerima = [nama_desa_penerima,nama_kecamatan_penerima,nama_kota_penerima,nama_provinsi_penerima]
					arr_pengirim = [nama_desa_pengirim,nama_kecamatan_pengirim,nama_kota_pengirim,nama_provinsi_pengirim]
				else:
					arr_pengirim = alamat1.split(",")
					arr_penerima = alamat2.split(",")

				coordinat_penerima, extra_cash_penerima, provinsi_penerima = get_location(arr_alamat=arr_penerima, URL_GEO=URL_GEO, API_GEO=API_GEO)
				coordinat_pengirim, extra_cash_pengirim, provinsi_pengirim = get_location(arr_alamat=arr_pengirim, URL_GEO=URL_GEO, API_GEO=API_GEO)
				
				data_extra_tarif_penerima = get_extra_tarif(extra_cash_penerima)
				# data_extra_tarif_pengirim = get_extra_tarif(extra_cash_pengirim)

				outlet_1 = get_outlet(coordinat_pengirim[1], coordinat_pengirim[0])
				outlet_2 = get_outlet(coordinat_penerima[1], coordinat_penerima[0])
				
				if outlet_1['data']['provinsi_toko_id'] is None:
					result['status'] = 404
					result['msg'] = 'Outlet Pengiriman tidak memiliki id provinsi'
					return JsonResponse({'result': result}, status=result['status'])
				if outlet_2['data']['provinsi_toko_id'] is None:
					result['status'] = 404
					result['msg'] = 'Outlet Penerimaan paket tidak memiliki id provinsi'

				lokasi_outlet_1 = np.array(outlet_1['data']['titik_lokasi'].split(',')).astype(np.float)
				lokasi_outlet_2 = np.array(outlet_2['data']['titik_lokasi'].split(',')).astype(np.float)

				# Pencarian Gudang menggunakan titik terdekat
				# =========================================================
				# titik_tengah_antar_outlet = get_center_coordinate(lokasi_outlet_1, lokasi_outlet_2)
				# titik_gd_1 = get_center_coordinate(lokasi_outlet_1, titik_tengah_antar_outlet)
				# titik_gd_2 = get_center_coordinate(lokasi_outlet_2, titik_tengah_antar_outlet)

				# gudang_1 = get_gudang(titik_gd_1[0], titik_gd_1[1])
				# gudang_2 = get_gudang(titik_gd_2[0], titik_gd_2[1])

				# lokasi_gudang_1 = np.array(gudang_1['data']['titik_lokasi'].split(',')).astype(np.float)
				# lokasi_gudang_2 = np.array(gudang_2['data']['titik_lokasi'].split(',')).astype(np.float)


				#pencarian gudang menggunakan pengambilan provinsi outlet
				#==========================================================
				#return JsonResponse({'result': 'Berhasil', 'gudang_1':outlet_1, 'gudang_2':outlet_2})
				try :
					gudang_1 = get_gudang_by_province(outlet_1['data']['provinsi_toko_id'])
					if not gudang_1['data'] :
						# titik_tengah_antar_outlet = get_center_coordinate(lokasi_outlet_1, lokasi_outlet_2)
						# gudang_1 = get_center_coordinate([float(outlet_1['data']['titik_lokasi'].split(',')[0]),float(outlet_1['data']['titik_lokasi'].split(',')[1])], titik_tengah_antar_outlet)
						uri_gudang_1 = str(request.build_absolute_uri('/admin/gudang/')) + str(outlet_1['data']['titik_lokasi'].split(',')[0]) + '/' + str(outlet_1['data']['titik_lokasi'].split(',')[1]) + '/'
						PARAMS = {}
						gudang_pengirim = req_api.get(url = uri_gudang_1, params = PARAMS)
						gudang_pengirim = gudang_pengirim.json()
						gudang_1 = gudang_pengirim
						lokasi_gudang_1 = np.array(gudang_1['data']['titik_lokasi'].split(',')).astype(np.float)
					else :
						lokasi_gudang_1 = np.array(gudang_1['data']['titik_lokasi'].split(',')).astype(np.float)

				except Exception as e:
					raise Exception('Tidak ada data Gudang terdekat outlet 1 tidak ditemukan')
				
				try :
					gudang_2 = get_gudang_by_province(outlet_2['data']['provinsi_toko_id'])
					if not gudang_2['data'] :
						# titik_tengah_antar_outlet = get_center_coordinate(lokasi_outlet_1, lokasi_outlet_2)
						# gudang_2 = get_center_coordinate([float(outlet_2['data']['titik_lokasi'].split(',')[0]),float(outlet_2['data']['titik_lokasi'].split(',')[1])], titik_tengah_antar_outlet)
						uri_gudang_2 = str(request.build_absolute_uri('/admin/gudang/')) + str(outlet_2['data']['titik_lokasi'].split(',')[0]) + '/' + str(outlet_2['data']['titik_lokasi'].split(',')[1]) + '/'
						PARAMS = {}
						gudang_pengirim = req_api.get(url = uri_gudang_2, params = PARAMS)
						gudang_penerima = gudang_penerima.json()
						gudang_2 = gudang_penerima
						lokasi_gudang_2 = np.array(gudang_2['data']['titik_lokasi'].split(',')).astype(np.float)
					else :
						lokasi_gudang_2 = np.array(gudang_2['data']['titik_lokasi'].split(',')).astype(np.float)

				except Exception as e:
					raise Exception('Tidak ada data Gudang terdekat outlet 2 tidak ditemukan')			


				# Check Lokasi Penerima & Pengirim apakah satu provinsi
				if provinsi_penerima == provinsi_pengirim:
					jarak_total = hitung_jarak(lokasi_outlet_1, [coordinat_penerima[1], coordinat_penerima[0]])
				else:
					jarak_total = hitung_jarak(lokasi_outlet_1, lokasi_gudang_1) + hitung_jarak(lokasi_gudang_2, [coordinat_penerima[1], coordinat_penerima[0]])

				data_pengemasan = get_harga_pengemasan(pengemasan)
				nama_pengemasan = data_pengemasan['nama_pengemasan']
				tarif_pengemasan = data_pengemasan['harga']
				tarif_kilometer = get_harga_kilometer(jarak_total)
				tarif_berat = get_harga_berat(berat)
				tarif_gudang = get_harga_gudang(gudang_1['data']['id'],gudang_2['data']['id'])
				# tarif_extra_pengirim = data_extra_tarif_pengirim['harga']
				if extra_tarif:
					tarif_extra_penerima = data_extra_tarif_penerima['harga']
				else:
					tarif_extra_penerima = 0

				final_result = get_list_layanan(tarif_berat, tarif_kilometer, tarif_gudang, tarif_pengemasan, tarif_extra_penerima)

				# result['data'] = {'lokasi_outlet_1': list(lokasi_outlet_1), 'coordinat_penerima': list(coordinat_penerima)}
				result['data'] = final_result['data']

				result['pengemasan'] = nama_pengemasan
				# result['tarif_berat'] = tarif_berat
				# result['tarif_kilometer'] = tarif_kilometer
				# result['tarif_gudang'] = tarif_gudang
				# result['tarif_pengemasan'] = tarif_pengemasan
				# result['extra_tarif_penerima'] = tarif_extra_penerima

				result['msg'] = 'Sukses'
		except Exception as e:
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 422

		return JsonResponse({'result': result}, status=result['status'])

def get_location_new(arr_coordinate1, arr_coordinate2, penerima_reverse=False):
	distance = 0
	api_key = CONF.API_OPEN_ROUTE_SERVICE
	if(penerima_reverse) :
		URL_GEO = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + str(arr_coordinate1[1]) + "," + str(arr_coordinate1[0]) + "&end=" + str(arr_coordinate2[0]) + "," + str(arr_coordinate2[1])
	else :
		URL_GEO = "https://api.openrouteservice.org/v2/directions/driving-car?api_key=" + api_key + "&start=" + str(arr_coordinate1[1]) + "," + str(arr_coordinate1[0]) + "&end=" + str(arr_coordinate2[1]) + "," + str(arr_coordinate2[0]);
	r = req_api.get(url = URL_GEO, params = {})
	data = r.json()
	if not len(data['features']) : # check jika kosong
		return distance
	else:
		try :
			distance = data['features'][0]['properties']['summary']['distance']
			print(distance)
		except :
			pass
	return distance

class CekTarifPelangganAPI(View):
	def get(self, request):
		URL_GEO = 'https://api.openrouteservice.org/geocode/search?'
		API_GEO = CONF.API_OPEN_ROUTE_SERVICE
		# result = {
		# 	'data': [],
		# 	'pengemasan': '',
		# 	'tarif_berat': 0,
		# 	'tarif_kilometer': 0,
		# 	'tarif_gudang': 0,
		# 	'tarif_pengemasan': 0,
		# 	# 'extra_tarif_pengirim': 0,
		# 	'extra_tarif_penerima': 0,
		# 	'msg': '',
		# 	'status': 200,
		# }
		result = {
			'data': [],
			'pengemasan': '',
			'msg': '',
			'status': 200,
		}
		nama_provinsi_penerima = ''
		nama_kota_penerima = ''
		nama_kecamatan_penerima = ''
		nama_desa_penerima = ''

		nama_provinsi_pengirim = ''
		nama_kota_pengirim = ''
		nama_kecamatan_pengirim = ''
		nama_desa_pengirim = ''

		try:
			# kode_pos_pengirim = request.GET.get('kode_pos_pengirim')
			# kode_pos_penerima = request.GET.get('kode_pos_penerima')

			alamat1 = request.GET.get('alamat_pengirim', '')
			alamat2 = request.GET.get('alamat_penerima', '')
			berat = float(request.GET.get('berat', 0))
			pengemasan = request.GET.get('pengemasan', 0)
			extra_tarif = request.GET.get('extra_tarif', False)
			# print("INI GET", alamat1, alamat2, berat)
			if alamat1 and alamat2 and berat:
				arr_pengirim = alamat1.split(",")
				arr_penerima = alamat2.split(",")

				coordinat_pengirim, extra_cash_pengirim, provinsi_pengirim = get_location(arr_alamat=arr_pengirim, URL_GEO=URL_GEO, API_GEO=API_GEO)
				coordinat_penerima, extra_cash_penerima, provinsi_penerima = get_location(arr_alamat=arr_penerima, URL_GEO=URL_GEO, API_GEO=API_GEO)
				
				data_extra_tarif_penerima = get_extra_tarif(extra_cash_penerima)
				# data_extra_tarif_pengirim = get_extra_tarif(extra_cash_pengirim)

				outlet_1 = get_outlet(coordinat_pengirim[1], coordinat_pengirim[0])
				outlet_2 = get_outlet(coordinat_penerima[1], coordinat_penerima[0])
				
				if outlet_1['data']['provinsi_toko_id'] is None:
					result['status'] = 404
					result['msg'] = 'Outlet Pengiriman tidak memiliki id provinsi'
					return JsonResponse({'result': result}, status=result['status'])
				if outlet_2['data']['provinsi_toko_id'] is None:
					result['status'] = 404
					result['msg'] = 'Outlet Penerimaan paket tidak memiliki id provinsi'
					return JsonResponse({'result': result}, status=result['status'])

				lokasi_outlet_1 = outlet_1['data']['titik_lokasi'].split(',')
				lokasi_outlet_2 = outlet_2['data']['titik_lokasi'].split(',')

				# Pencarian Gudang menggunakan titik terdekat
				# =========================================================
				# titik_tengah_antar_outlet = get_center_coordinate(lokasi_outlet_1, lokasi_outlet_2)
				# titik_gd_1 = get_center_coordinate(lokasi_outlet_1, titik_tengah_antar_outlet)
				# titik_gd_2 = get_center_coordinate(lokasi_outlet_2, titik_tengah_antar_outlet)

				# gudang_1 = get_gudang(titik_gd_1[0], titik_gd_1[1])
				# gudang_2 = get_gudang(titik_gd_2[0], titik_gd_2[1])

				# lokasi_gudang_1 = np.array(gudang_1['data']['titik_lokasi'].split(',')).astype(np.float)
				# lokasi_gudang_2 = np.array(gudang_2['data']['titik_lokasi'].split(',')).astype(np.float)


				#pencarian gudang menggunakan pengambilan provinsi outlet
				#==========================================================

				gudang_1 = get_gudang_by_province(outlet_1['data']['provinsi_toko_id'])
				gudang_2 = get_gudang_by_province(outlet_2['data']['provinsi_toko_id'])
				lokasi_gudang_1 = gudang_1['data']['titik_lokasi'].split(',')
				lokasi_gudang_2 = gudang_2['data']['titik_lokasi'].split(',')

				try :
					outlet1_gudang1 = get_location_new(lokasi_outlet_1, lokasi_gudang_1)
					gudang1_gudang2 = get_location_new(lokasi_gudang_1, lokasi_gudang_2)
					gudang2_outlet2 = get_location_new(lokasi_gudang_2, lokasi_outlet_2)
					outlet2_penerima = get_location_new(lokasi_outlet_2, coordinat_penerima, True)
				except :
					try :
						outlet1_gudang1 = hitung_jarak(lokasi_outlet_1, lokasi_gudang_1)
						gudang1_gudang2 = hitung_jarak(lokasi_gudang_1, lokasi_gudang_2)
						gudang2_outlet2 = hitung_jarak(lokasi_gudang_2, lokasi_outlet_2)
						outlet2_penerima = hitung_jarak(lokasi_outlet_2, coordinat_penerima, True)
					except :
						outlet1_gudang1 = 0
						gudang1_gudang2 = 0
						gudang2_outlet2 = 0
						outlet2_penerima = 0


				# Check Lokasi Penerima & Pengirim apakah satu provinsi
				# if provinsi_penerima == provinsi_pengirim:
				# 	jarak_total = hitung_jarak(lokasi_outlet_1, [coordinat_penerima[1], coordinat_penerima[0]])
				# else:
				# jarak_total = hitung_jarak(lokasi_outlet_1, lokasi_gudang_1) + hitung_jarak(lokasi_gudang_2, [coordinat_penerima[1], coordinat_penerima[0]])
				jarak_total = (float(outlet1_gudang1) + float(gudang1_gudang2) + float(gudang2_outlet2) + float(outlet2_penerima)) / 1000

				data_pengemasan = get_harga_pengemasan(pengemasan)
				nama_pengemasan = data_pengemasan['nama_pengemasan']
				tarif_pengemasan = data_pengemasan['harga']
				tarif_kilometer = get_harga_kilometer_new(jarak_total)
				tarif_berat = get_harga_berat_new(berat)
				tarif_gudang = get_harga_gudang(gudang_1['data']['id'],gudang_2['data']['id'])
				# tarif_extra_pengirim = data_extra_tarif_pengirim['harga']
				if extra_tarif:
					tarif_extra_penerima = data_extra_tarif_penerima['harga']
				else:
					tarif_extra_penerima = 0

				final_result = get_list_layanan(tarif_berat, tarif_kilometer, tarif_gudang, tarif_pengemasan, tarif_extra_penerima)

				# result['data'] = {'lokasi_outlet_1': list(lokasi_outlet_1), 'coordinat_penerima': list(coordinat_penerima)}
				result['data'] = final_result['data']
				result['berat_input'] = {
					'berat': berat, 
					'satuan': 'Kg'
				}
				result['pengemasan'] = nama_pengemasan
				result['tarif_berat'] = tarif_berat
				result['tarif_kilometer'] = tarif_kilometer
				result['tarif_gudang'] = tarif_gudang
				result['tarif_pengemasan'] = tarif_pengemasan
				result['extra_tarif_penerima'] = tarif_extra_penerima

				result['msg'] = 'Sukses'
			else :
				result['msg'] = 'Error'
				result['status'] = 400
				result['error_detail'] = 'Alamat Pengirim, Penerima dan Berat tidak boleh kosong'
		except Exception as e:
			result['msg'] = 'Terjadi Kesalahan: {}'.format(e)
			result['status'] = 422

		return JsonResponse({'result': result}, status=result['status'])

class PaketInvoice(APIView):
	def post(self, request, *args, **kwargs):
# 		pengiriman = get_object_or_404(Pengiriman, id_pengiriman=request.POST.get('id_pengiriman'))
        # print(id_pengiriman)
		pengiriman_awal = Pengiriman.objects.get(id_pengiriman=request.POST.get('id_resi'))
		pengiriman = ambil_data(get_object_or_404(Pengiriman, id=pengiriman_awal.id))
		rute_pengiriman = LogPengiriman.objects.filter(id_pengiriman=pengiriman_awal.id).first()
		log_pengiriman = LogPengiriman.objects.filter(id_pengiriman=pengiriman_awal.id).values()
		# print(list(log_pengiriman))

		if rute_pengiriman.id_kurir:
			kurir_pengiriman = ambil_kurir(get_object_or_404(User, id=rute_pengiriman.id_kurir.id))
		else:
			kurir_pengiriman = ambil_kurir('')
		rute = ambil_rute(rute_pengiriman)
		status_pengiriman = ambil_status(LogPengiriman.objects.filter(id_pengiriman=pengiriman_awal.id).order_by('-created_at')[0])
		data = {'data': pengiriman, 'rute': rute, 'kurir': kurir_pengiriman, 'status': status_pengiriman, 'log': list(log_pengiriman)}
		print('TEST PENGIRIMAN', data)
		return JsonResponse({'results': data})

