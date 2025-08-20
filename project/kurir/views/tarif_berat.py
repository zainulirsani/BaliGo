from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

import math
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
class KurirTarifBeratView(View):
	def get(self, request):
		tarif_berat = list(TarifBerat.objects.filter(is_active=True).values())
		data_list = []
		data_tarif_berat = []
		i = 1
		for data in tarif_berat:
			data_list = [data['id_tarif_berat']]
			data_list.append(str(data['berat']) + ' Kg')
			data_list.append('Rp. ' + str(data['tarif']))
			data_tarif_berat.extend([data_list])

		if request.is_ajax():
			return JsonResponse({'data': data_tarif_berat}, status=200)

		return render(request, 'mobile_kurir/templates/tarif_berat/index.html', context={'tarif_berat': data_tarif_berat, 'is_active_tarif':'active'})