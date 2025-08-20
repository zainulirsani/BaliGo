from rest_framework import filters
from rest_framework import generics
from ..models import Toko
from ..serializers import TokoSerializer
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Q

from .custom_decorator import *

class TokoAPIView(generics.ListCreateAPIView):
    search_fields = ['nama_toko', 'alamat']
    filter_backends = (filters.SearchFilter,)
    queryset = Toko.objects.filter(is_active=True)
    serializer_class = TokoSerializer


class TokoToSelect2(View):
	def get(self, request):

		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET['page'])
			total_counts = Toko.objects.filter(Q(is_active=True) & (Q(nama_toko__icontains=q) | Q(alamat__icontains=q))).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Toko.objects.values().filter(Q(is_active=True) & (Q(nama_toko__icontains=q) | Q(alamat__icontains=q)))[start_p:pages])
			
		else:
			page = int(request.GET['page'])
			total_counts = Toko.objects.filter(is_active = True).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Toko.objects.values().filter(is_active = True)[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': (data['nama_toko'] + " | Alamat : " + data['alamat']) })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)