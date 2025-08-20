from rest_framework import serializers
from ..models import Toko
class TokoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toko
        fields = '__all__'