from rest_framework import serializers
from ..models import Gudang
class GudangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gudang
        fields = '__all__'