from rest_framework import serializers
from inventario.models import Marca

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre']
        read_only_fields = ['id']

    def validate_nombre(self, value):
        nombre_limpio = value.strip().upper()
        return nombre_limpio