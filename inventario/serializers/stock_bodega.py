from rest_framework import serializers
from inventario.models import StockBodega

class StockBodegaSerializer(serializers.ModelSerializer):
    bodega_nombre = serializers.CharField(source='bodega.nombre', read_only=True)
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = StockBodega
        fields = ['id', 'bodega', 'bodega_nombre', 'producto', 'producto_nombre', 'cantidad']
        read_only_fields = ['id', 'bodega_nombre', 'producto_nombre']

    def validate_cantidad(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        return value