from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.db.models import Q

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


def generate_id(path, len):
	data = path + "-{0}{1}".format(datetime.datetime.now().strftime("%y%d%S").zfill(len),randint(1,9))
	return data

@method_decorator(login_required, name='get')
class KurirTarifGudangView(View):
	def get(self, request):
		tarif_gudang = list(TarifGudang.objects.filter(is_active=True).values())
		data_list = []
		data_tarif_gudang = []
		i = 1
		for data in tarif_gudang:
			data_list = [data['id_tarif_gudang']]
			try:
				from_gudang = model_to_dict(get_object_or_404(Gudang, id = data['from_gudang_id']))
				data_list.append(from_gudang['nama_gudang'])
			except:
				data_list.append('Kosong')

			try:
				to_gudang = model_to_dict(get_object_or_404(Gudang, id = data['to_gudang_id']))
				data_list.append(to_gudang['nama_gudang'])
			except:
				data_list.append('Kosong')

			data_list.append('Rp. ' + str(data['tarif']))

			i =  i+1
			data_tarif_gudang.extend([data_list])
		print(data_tarif_gudang)

		if request.is_ajax():
			return JsonResponse({'data': data_tarif_gudang}, status=200)

		return render(request, 'mobile_kurir/templates/tarif_gudang/index.html', context={'tarif_gudang': data_tarif_gudang, 'is_active_tarif':'active'})