from rest_framework import filters
from rest_framework import generics
from ..models import Layanan
from ..serializers import LayananSerializer
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q

class LayananAPIView(generics.ListCreateAPIView):
    search_fields = ['nama_layanan', 'deskripsi', 'estimasi_layanan']
    filter_backends = (filters.SearchFilter,)
    queryset = Layanan.objects.filter(is_active=True)
    renderer_classes = [JSONRenderer]
    serializer_class = LayananSerializer


class LayananToSelect2(View):
	def get(self, request):

		if request.GET.get('q'):
			q = request.GET['q']
			page = int(request.GET['page'])
			total_counts = Layanan.objects.filter(Q(is_active=True) & Q(publish_status=True) & (Q(nama_layanan__icontains=q) | Q(deskripsi__icontains=q) | Q(estimasi_layanan__icontains=q))).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0

			datas = list(Layanan.objects.values().filter(Q(is_active=True) & Q(publish_status=True) & (Q(nama_layanan__icontains=q) | Q(deskripsi__icontains=q) | Q(estimasi_layanan__icontains=q)))[start_p:pages])
			
		else:
			page = int(request.GET['page'])
			total_counts = Layanan.objects.filter(Q(is_active = True) & Q(publish_status=True)).count()

			pages = page * 10
			if pages > total_counts:
				pages = total_counts

				start_p = (page - 1) * 10
			else:
				if pages > 10:
					start_p = pages - 10
				else:
					start_p = 0
				
			datas = list(Layanan.objects.values().filter(Q(is_active = True) & Q(publish_status=True))[start_p:pages])
			

		data_list = []
		i = 1
		for data in datas:

			data_list.append({'id': data['id'], 'text': (data['nama_layanan'] + " || " + str(int(data['estimasi_layanan'])) + ' Hari') })
		
		return JsonResponse({'results': data_list, 'total_count': total_counts}, safe=False)