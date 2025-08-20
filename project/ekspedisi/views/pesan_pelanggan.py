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
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core.mail import send_mail

from .custom_decorator import *

def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

class PesanView(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request):
		form = PesanPelangganForm()
		form_balasan = BalasanPesanPelangganForm()
		pesan = PesanPelanggan.objects.all()
		datas = list(PesanPelanggan.objects.values().filter(is_active = True))
		data_list = []
		data_pesan = []
		i = 1
		for data in datas:
			data_list = [i]
			data_list.append(data['nama'])
			data_list.append(data['email'])
			data_list.append(data['no_hp'])
			data_list.append(data['judul'])
			data_list.append('<center><div class="btn-group" role="group"><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Balas Pesan" data-id="' + str(data['id']) + '" class="btn btn-info btn-sm balasPesan"><i class="fa fa-fw fa-edit"></i> Balas</a><a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Hapus Pesan" data-id="' + str(data['id']) + '" data-nama="' + str(data['nama']) +' | '+ str(data['judul']) +'"class="btn btn-danger btn-sm deletePesan"><i class="fa fa-fw fa-trash-alt"></i> Hapus</a></div><center>')
			i =  i+1
			data_pesan.extend([data_list])
		if request.is_ajax():
			return JsonResponse({'data': data_pesan}, status=200)

		return render(request, 'pesan/index.html', context={'form': form, 'form_balasan': form_balasan, 'pesan': pesan})

	@csrf_exempt
	def post(self, request):
		form = BalasanPesanPelangganForm(request.POST)
		if form.is_valid():
			try:
				pesan_dari_pelanggan = get_object_or_404(PesanPelanggan, id=request.POST.get('pesan_pelanggan'))
				report = send_mail('Tanggapan: '+pesan_dari_pelanggan.judul,
					request.POST.get('balasan'),
					'admin@samitra.com',
					[pesan_dari_pelanggan.email],
					fail_silently=False,
					)
				tz = get_current_timezone()
				new_balasan = form.save()
				if report:
					msg_report = 'Email Terkirim!'
				else:
					msg_report = 'Email Gagal Terkirim!'
				return JsonResponse({'balasan': model_to_dict(new_balasan), 'msg': 'Berhasil Menyimpan Balasan dan '+msg_report, 'type': 'success'}, status=200)
			except:
				return JsonResponse({'msg': 'Gagal Menyimpan Balasan', 'type': 'error'}, status=200)
		else:
			return JsonResponse({'msg': 'Gagal Menyimpan Balasan, pastikan data yang dibutuhkan sudah terisi', 'type': 'error'}, status=422)

class PesanBalas(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def get(self, request, id):
		try:
			pesan = get_object_or_404(PesanPelanggan, id = id)
			datas = list(BalasanPesanPelanggan.objects.values().filter(is_active = True, pesan_pelanggan_id = id))
			data_list = []
			data_balasan = []
			i = 1
			for data in datas:
				data_list = [i]
				data_list.append(data['balasan'])
				data_list.append(data['created_at'])
				i =  i+1
				data_balasan.extend([data_list])

			return JsonResponse({'data': model_to_dict(pesan), 'data_balasan': data_balasan, 'msg': 'Berhasil Mengambil Data pesan', 'type': 'success'})
		except:
			return JsonResponse({'msg': 'Gagal Mengambil Data pesan', 'type': 'error'})

class PesanDelete(View):
	@method_decorator(super_admin_check(path_url='/page_not_found/'))
	def post(self, request, id):
		pesan = PesanPelanggan.objects.get(id=id)
		try:
			pesan.is_active = False
			pesan.save()
			return JsonResponse({'msg': 'Berhasil Menghapus Data pesan (Arsip)', 'type': 'success'}, status=200)
		except:
			return JsonResponse({'msg': 'Gagal Mengapus Data pesan (Arsip)', 'type': 'error'}, status=443)