from rest_framework import serializers
from inventario.models import NumeroSerie

class NumeroSerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumeroSerie
        fields = '__all__'