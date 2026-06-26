from rest_framework import serializers
from inventario.models import AlertaStockMinimo

class AlertaStockMinimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertaStockMinimo
        fields = '__all__'