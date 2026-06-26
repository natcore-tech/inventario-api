from rest_framework import serializers
from django.db import transaction
from inventario.models import Cotizacion, CotizacionDetalle

class CotizacionDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CotizacionDetalle
        fields = ['producto', 'cantidad', 'precio_propuesto']

class CotizacionSerializer(serializers.ModelSerializer):
    detalles = CotizacionDetalleSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = ['proveedor', 'codigo_cotizacion', 'fecha_validez', 'total_propuesto', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        with transaction.atomic():
            cotizacion = Cotizacion.objects.create(**validated_data)
            for detalle in detalles_data:
                CotizacionDetalle.objects.create(cotizacion=cotizacion, **detalle)
        return cotizacion