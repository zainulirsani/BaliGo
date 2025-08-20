from rest_framework import serializers
from ..models import Satuan
class SatuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satuan
        fields = '__all__'