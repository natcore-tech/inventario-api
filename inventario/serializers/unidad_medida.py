from rest_framework import serializers
from inventario.models import UnidadMedida


class UnidadMedidaSerializer(serializers.ModelSerializer):
    descripcion_completa = serializers.SerializerMethodField()

    class Meta:
        model = UnidadMedida
        fields = ['id', 'nombre', 'abreviatura', 'descripcion_completa']
        read_only_fields = ['id', 'descripcion_completa']

    def get_descripcion_completa(self, obj) -> str:
        # Ahora arma un bonito "Kilogramo (kg)" en vez de multiplicar fantasmas
        return f"{obj.nombre} ({obj.abreviatura})"

    def validate_nombre(self, value):
        return value.strip().capitalize()