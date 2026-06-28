from rest_framework import serializers
from inventario.models import UnidadMedida

class UnidadMedidaSerializer(serializers.ModelSerializer):
    descripcion_completa = serializers.SerializerMethodField()

    class Meta:
        model = UnidadMedida
        fields = ['id', 'nombre', 'cantidad_por_unidad', 'descripcion_completa']
        read_only_fields = ['id', 'descripcion_completa']

    def get_descripcion_completa(self, obj):
        if obj.cantidad_por_unidad > 1:
            return f"{obj.nombre} de {obj.cantidad_por_unidad}"
        return obj.nombre

    def validate_cantidad_por_unidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad por unidad debe ser estrictamente mayor a cero.")
        return value

    def validate_nombre(self, value):
        return value.strip().capitalize()