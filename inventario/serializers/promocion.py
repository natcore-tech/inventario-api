# inventario/serializers/promocion.py
from rest_framework import serializers
from inventario.models import Promocion


class PromocionSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = Promocion
        fields = [
            'id', 
            'nombre', 
            'producto', 
            'nombre_producto',
            'porcentaje_descuento', 
            'fecha_inicio', 
            'fecha_fin', 
            'es_activa', 
            'creado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'nombre_producto']

    def validate_porcentaje_descuento(self, valor):
        if valor <= 0 or valor > 100:
            raise serializers.ValidationError("El porcentaje de descuento debe ser mayor a 0 y máximo 100.")
        return valor

    def validate(self, datos):
        inicio = datos.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        fin = datos.get('fecha_fin', getattr(self.instance, 'fecha_fin', None))

        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({
                "fecha_fin": "La fecha de finalización no puede ser anterior a la fecha de inicio."
            })
            
        return datos