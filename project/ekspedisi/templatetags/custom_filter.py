import json
import ast
from django import template
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from datetime import datetime
from ekspedisi.models import Toko, Gudang
import html

register = template.Library()
nameToIcon = list(['approved_status', 'iuu_list', 'code_of_conduct'])

@register.filter
def get_obj_attr(obj) :
	return dir(obj)

@register.filter
def get_log(obj, id) :
	data = obj.log_pengiriman.all().last()
	to_return = ''
	titik_lokasi = 'Tidak diketahui'
	if(data.status_pengiriman == 'waiting') :
		to_return = '<h5 class="widget-user-desc"><i class="fas fa-clock"></i>&nbsp;&nbsp;Menunggu dikirim</h5>'
	elif (data.status_pengiriman == 'sent_by') :
		to_return = '<h5 class="widget-user-desc"><i class="fas fa-plane"></i>&nbsp;&nbsp;Dikirim</h5>'
	elif (data.status_pengiriman == 'arrive_at') :
		try :
			titik_lokasi = data.titik_lokasi
			outlet = Toko.objects.get(titik_lokasi=titik_lokasi)
			titik_lokasi = outlet.nama_toko
		except Toko.DoesNotExist :
			try :
				gudang = Gudang.objects.get(titik_lokasi=titik_lokasi)
				titik_lokasi = 'Gudang '+gudang.nama_gudang
			except :
				pass
			
		to_return = '<h5 class="widget-user-desc"><i class="fas fa-check"></i>&nbsp;&nbsp;Sampai di {}</h5>'.format(str(titik_lokasi))
	elif (data.status_pengiriman == 'done') :
		to_return = '<h5 class="widget-user-desc"><i class="fas fa-check-square"></i>&nbsp;&nbsp;Pengiriman Selesai</h5>'
	else :
		to_return = '<h5 class="widget-user-desc"><i class="fas fa-window-close"></i>&nbsp;&nbsp;Status tidak diketahui</h5>'

	return to_return

@register.filter
def get_penempatan(obj) :
	if hasattr(obj, 'penempatan_toko') and obj.penempatan_toko :
		return str(obj.penempatan_toko.nama_toko)
	elif hasattr(obj, 'penempatan_gudang') and obj.penempatan_gudang :
		return str(obj.penempatan_gudang.nama_gudang)

@register.filter
def cek_posisi(obj) :
	switcher = {
		"adm_gudang" : "Admin Gudang",
		"adm_outlet" : "Admin Outlet",
		"kurir" : "Kurir"
	}
	if(hasattr(obj, 'role')) :
		role = obj.role
		role_is = switcher.get(role, None)
		if role_is :
			return "&emsp;|&emsp;{role_to_display}".format(role_to_display=role_is)
		elif obj.is_staff :
			return "&emsp;|&emsp;Superuser"
	return ''
