from rest_framework import serializers
from ..models import Pengemasan
class PengemasanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengemasan
        fields = '__all__'