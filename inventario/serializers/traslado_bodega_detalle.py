from rest_framework import serializers
from inventario.models import TrasladoBodegaDetalle

class TrasladoBodegaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrasladoBodegaDetalle
        fields = ['id', 'traslado', 'producto', 'cantidad']
        read_only_fields = ['id', 'traslado']

    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value