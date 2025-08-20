from rest_framework import filters
from rest_framework import generics
from ..models import JenisKiriman
from ..serializers import JenisKirimanSerializer
from django.views.generic import View
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from django.db.models import Q

class JenisKirimanAPIView(generics.ListCreateAPIView):
    search_fields = ['nama']
    filter_backends = (filters.SearchFilter,)
    queryset = JenisKiriman.objects.filter(is_active=True)
    renderer_classes = [JSONRenderer]
    serializer_class = JenisKirimanSerializer