from rest_framework import serializers
from inventario.models import Bodega

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = ['id', 'nombre', 'direccion', 'activa']
        read_only_fields = ['id']

    def validate_nombre(self, value):
        return value.strip().upper()