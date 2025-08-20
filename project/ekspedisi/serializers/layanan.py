from rest_framework import serializers
from ..models import Layanan
class LayananSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layanan
        fields = '__all__'