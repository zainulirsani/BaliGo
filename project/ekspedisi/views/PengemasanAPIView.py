from rest_framework import filters
from rest_framework import generics
from ..models import Pengemasan
from ..serializers import PengemasanSerializer
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
import ast

class PengemasanAPIView(generics.ListCreateAPIView):
    search_fields = ['nama_pengemasan', 'bahan_pengemasan']
    filter_backends = (filters.SearchFilter,)
    queryset = Pengemasan.objects.filter(is_active=True)
    serializer_class = PengemasanSerializer
    renderer_classes = [JSONRenderer,]


class PengemasanToSelect2(View):
	def get(self, request):

		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET['page'])
			total_counts = Pengemasan.objects.filter(Q(is_active=True) & (Q(nama_pengemasan__icontains=q) | Q(bahan_pengemasan__icontains=q))).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Pengemasan.objects.values().filter(Q(is_active=True) & (Q(nama_pengemasan__icontains=q) | Q(bahan_pengemasan__icontains=q)))[start_p:pages])
			
		else:
			page = int(request.GET['page'])
			total_counts = Pengemasan.objects.filter(is_active = True).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Pengemasan.objects.values().filter(is_active = True)[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': (data['nama_pengemasan'] + " || " + data['bahan_pengemasan']) })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)


class PengemasanDetailAPI(View):
	def post(self, request, id_pengemasan):
		try:
			data = get_object_or_404(Pengemasan, id = id_pengemasan)
			return JsonResponse({'data': model_to_dict(data), 'msg': 'Berhasil Mengambil Detail Pengemasan', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'data': '', 'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)

	def get(self, request, id_pengemasan):
		try:
			data = get_object_or_404(Pengemasan, id = id_pengemasan)
			return JsonResponse({'data': model_to_dict(data), 'msg': 'Berhasil Mengambil Detail Pengemasan', 'type': 'success'}, status=200)
		except Exception as e:
			return JsonResponse({'data': '', 'msg': 'Terjadi Kesalahan {}'.format(e), 'type': 'error'}, status=400)