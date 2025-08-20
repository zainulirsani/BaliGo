from rest_framework import serializers
from ..models import JenisKiriman
class JenisKirimanSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisKiriman
        fields = '__all__'