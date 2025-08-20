from rest_framework import serializers
from ..models import Provinsi
class ProvinsiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provinsi
        fields = '__all__'