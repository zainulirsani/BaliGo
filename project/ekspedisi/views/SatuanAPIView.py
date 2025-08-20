from rest_framework import filters
from rest_framework import generics
from ..models import Satuan
from ..serializers import SatuanSerializer
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q

class SatuanAPIView(generics.ListCreateAPIView):
    search_fields = ['nama_satuan']
    filter_backends = (filters.SearchFilter,)
    queryset = Satuan.objects.filter(is_active=True)
    renderer_classes = [JSONRenderer]
    serializer_class = SatuanSerializer