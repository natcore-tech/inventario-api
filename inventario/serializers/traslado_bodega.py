from rest_framework import serializers
from django.db import transaction
from inventario.models import TrasladoBodega, TrasladoBodegaDetalle
from .traslado_bodega_detalle import TrasladoBodegaDetalleSerializer

class TrasladoBodegaSerializer(serializers.ModelSerializer):
    detalles = TrasladoBodegaDetalleSerializer(many=True)
    bodega_origen_nombre = serializers.CharField(source='bodega_origen.nombre', read_only=True)
    bodega_destino_nombre = serializers.CharField(source='bodega_destino.nombre', read_only=True)

    class Meta:
        model = TrasladoBodega
        fields = [
            'id', 'fecha_traslado', 'bodega_origen', 'bodega_origen_nombre',
            'bodega_destino', 'bodega_destino_nombre', 'estado', 'detalles'
        ]
        read_only_fields = ['id', 'fecha_traslado', 'estado']

    def validate(self, data):
        if data.get('bodega_origen') == data.get('bodega_destino'):
            raise serializers.ValidationError({
                "bodega_destino": "La bodega de destino no puede ser igual a la de origen."
            })
        return data

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        traslado = TrasladoBodega.objects.create(**validated_data)
        
        detalles_crear = [
            TrasladoBodegaDetalle(traslado=traslado, **detalle)
            for detalle in detalles_data
        ]
        TrasladoBodegaDetalle.objects.bulk_create(detalles_crear)
        
        return traslado