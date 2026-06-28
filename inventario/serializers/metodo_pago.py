# inventario/serializers/metodo_pago.py
from rest_framework import serializers
from inventario.models import MetodoPago


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ['id', 'nombre', 'es_activo', 'creado_en', 'actualizado_en']
        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def validate_nombre(self, valor):
        nombre = valor.strip()
        
        # Validación insensible a mayúsculas/minúsculas
        consulta = MetodoPago.objects.filter(nombre__iexact=nombre)
        if self.instance:
            consulta = consulta.exclude(pk=self.instance.pk)
            
        if consulta.exists():
            raise serializers.ValidationError("Ya existe un método de pago con este nombre.")
            
        return nombre